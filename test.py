# -*- coding: utf-8 -*-
import time
import requests
import pymysql
from common import Global
import threading
import re
'''
每个线程首先从origin表中取20条数据进行测试，并将其从origin删除
测试20条代理的可用性和连接速度并存入aviable表
'''
lock = threading.Lock()
def test(conn,num=10):
    start_time = time.time()
    interval = 30  # 爬取间隔 尽可能在此间隔内完成任务
    while True:
        now_time = time.time()
        if (now_time-start_time) > (interval*60-num*2*10):        #马上就要超时，不重启
            break
        try:
            cursor = conn.cursor()
            sql = "SELECT COUNT(*) FROM origin"
            lock.acquire()
            cursor.execute(sql)
            lock.release()
            res = cursor.fetchone()  # 抓取待测试代理数
            if res[0] == 0:                                        #空退出
                break
            sql = "select IP,PORT,ID from origin order by UPDATE_TIME desc limit {}".format(num)
            lock.acquire()
            cursor.execute(sql)
            lock.release()
            results = cursor.fetchall()
            for proxy in results:
                sql = "delete from origin where ID={}".format(proxy[2])  # 删除之前获取的记录
                lock.acquire()
                cursor.execute(sql)
                lock.release()
            validIp = []  # 成功的代理\
            start_test_time = time.time()
            for proxy in results:
                res = test_ip(proxy[0], proxy[1])
                if res != False:
                    dic = {}
                    dic['ip'] = proxy[0]
                    dic['port'] = proxy[1]
                    dic['speed'] = res
                    validIp.append(dic)
            thread = threading.current_thread()
            print('[INFO] ' + thread.getName() + ' has finished his work. Successfully get {} proxy cost {}s '.format(
                validIp.__len__(),time.time()-start_test_time))
            save(validIp, conn)
            cursor.close()
        except Exception as e:
            print(e)

def test_ip(ip,port):
    proxies = {'https': str(ip)+":"+str(port)}
    start = time.time()
    try:
        response = requests.get('https://www.bilibili.com/12',timeout=10,proxies=proxies)  #超过10s的代理抛弃
        cost = time.time() - start
        cost = round(cost,2)        #保留两位小数
        result = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", response.text)
        if result[0] != Global.get_value('local_ip'):
            return cost
        else:
            return False
    except Exception as e:
        return False

def save(validIp,conn):
    try:
        cursor = conn.cursor()
        for ip in validIp:
            #replace into 保证不会插入重复ip，且已存在该ip时执行更新操作
            sql = "REPLACE INTO available(IP, PORT, UPDATE_TIME,SPEED) VALUES ('{}',{},unix_timestamp(),{})".format(ip['ip'],str(ip['port']),str(ip['speed']))
            lock.acquire()
            cursor.execute(sql)
            lock.release()
        cursor.close()
    except Exception as e:
        print(e)
        print("[ERROR] Failed to save effective proxy data")


def start_test():
    conn = pymysql.connect(host=Global.get_value('host'), user=Global.get_value('user'),
                           passwd=Global.get_value('password'), db=Global.get_value('dbname'),
                           port=Global.get_value('port'), charset='utf8',autocommit = True)

    threadpool = []
    for i in range(5):
        th = threading.Thread(target=test, args=(conn,), name='thread-test-ip-' + str(i))
        threadpool.append(th)
        print('[INFO] Start thread-test-ip-' + str(i) + ' to test proxy')
        th.start()
        time.sleep(1)       #保证子线程已经获取删除数据
    for th in threadpool:
        threading.Thread.join(th)
    print('[INFO] '+'All thread-test-ip have finshed at '+time.ctime())
    conn.close()        #关闭数据库连接

def cycle_test(interval = 10):
    print("[INFO] Open the thread to test ip from table 'origin' every {} minutes".format(interval))
    while True:
        time.sleep(interval*60)   #休眠interval*60s
        conn = pymysql.connect(host=Global.get_value('host'), user=Global.get_value('user'),
                               passwd=Global.get_value('password'), db=Global.get_value('dbname'),
                               port=Global.get_value('port'), charset='utf8')
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM origin"
        cursor.execute(sql)
        res = cursor.fetchone()  # 抓取待测试代理数
        cursor.close()
        conn.close()
        if res[0] == 0:
            print("[INFO] The 'origin' table is empty. thread-test-ip continues sleeping")
        else:
            print("[INFO] Begin to test ip from table 'origin' at {}".format(time.ctime()))
            start_test()
        print("[INFO] thread-test-ip is sleeping")
