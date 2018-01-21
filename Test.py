# -*- coding: utf-8 -*-
import time
import requests
import pymysql
from common import Global
import threading
'''
首先从origin表中取10条数据进行测试，并将其从origin删除
测试10条代理的可用性和连接速度并存入aviable表
'''

def start_test():      #默认一次取10条
    conn = pymysql.connect(host=Global.get_value('host'), user=Global.get_value('user'),
                           passwd=Global.get_value('password'), db=Global.get_value('dbname'),
                           port=Global.get_value('port'), charset='utf8')

    threadpool = []
    for i in range(3):
        th = threading.Thread(target=test, args=(conn,), name='thread-' + str(i))
        threadpool.append(th)
        th.start()
        print('[INFO] Start thread-'+ str(i)+' to test proxy')
        time.sleep(1)       #保证子线程已经获取删除数据
    for th in threadpool:
        threading.Thread.join(th)
    print('[INFO] '+'All threads have finshed at '+time.ctime())
    conn.close()        #关闭数据库连接

def test(conn,num=10):
    try:
        cursor = conn.cursor()
        sql = "select IP,PORT,ID from origin order by UPDATE_TIME desc limit {}".format(num)
        cursor.execute(sql)
        results = cursor.fetchall()
        for proxy in results:
            sql = "delete from origin where ID={}".format(proxy[2])  # 删除之前获取的记录
            cursor.execute(sql)
        validIp = []  # 成功的代理
        for proxy in results:
            res = test_ip(proxy[0],proxy[1])
            if res != False:
                dic = {}
                dic['ip'] = proxy[0]
                dic['port'] = proxy[1]
                dic['speed'] = res
                validIp.append(dic)
        thread = threading.current_thread()
        print('[INFO] '+thread.getName()+' has finished his work. Successfully get {} proxy'.format(validIp.__len__()))
        save(validIp,conn)
        cursor.close()
    except Exception as e:
        print(e)

def test_ip(ip,port):
    proxies = {'http': str(ip)+":"+str(port)}
    start = time.time()
    try:
        requests.get('http://www.baidu.com',timeout=20,proxies=proxies)
        cost = time.time() - start
        cost = round(cost,2)        #保留两位小数
        return cost
    except Exception as e:
        return False

def save(validIp,conn):
    try:
        cursor = conn.cursor()
        for ip in validIp:
            #replace into 保证不会插入重复ip，且已存在该ip时执行更新操作
            sql = "REPLACE INTO available(IP, PORT, UPDATE_TIME,SPEED) VALUES ('" + ip['ip'] + "'," + str(ip['port']) + ",unix_timestamp(),"+str(ip['speed']) + ')'
            cursor.execute(sql)
        cursor.close()
        return True
    except Exception as e:
        print(e)
        print("[ERROR] Failed to save effective proxy data")
        return False


