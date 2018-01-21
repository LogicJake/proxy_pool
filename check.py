# -*- coding: utf-8 -*-
import time
import requests
import pymysql
from common import Global
import threading
'''
检查available表中有没有代理失效，优先检查时间久的
'''

def check(conn,num=10):
    try:
        cursor = conn.cursor()
        sql = "select IP,PORT,ID from available WHERE STATUS=0 order by UPDATE_TIME limit {} ".format(num)   #获取num条数据
        cursor.execute(sql)
        results = cursor.fetchall()
        for proxy in results:
            sql = "update available SET STATUS=1 WHERE ID={}".format(proxy[2])  # 状态设置为1，表示正在被检查
            cursor.execute(sql)
        num = 0
        for proxy in results:
            res = test_ip(proxy[0],proxy[1])
            if res == False:
                num = num+1
                sql = "delete from available where ID={}".format(proxy[2])  # 删除失效代理
                cursor.execute(sql)
            else:            #更新数据
                sql = "update available SET UPDATE_TIME=unix_timestamp(), SPEED={}, STATUS=0 WHERE ID={}".format(res,proxy[2])
                cursor.execute(sql)
        thread = threading.current_thread()
        print('[INFO] '+thread.getName()+' has finished his work. Successfully delete {} invalid proxy'.format(num))
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

def start_check():      #默认一次取10条
    conn = pymysql.connect(host=Global.get_value('host'), user=Global.get_value('user'),
                           passwd=Global.get_value('password'), db=Global.get_value('dbname'),
                           port=Global.get_value('port'), charset='utf8')

    threadpool = []
    for i in range(3):
        th = threading.Thread(target=check, args=(conn,), name='thread-check-ip-' + str(i))
        threadpool.append(th)
        th.start()
        print('[INFO] Start thread-check-ip-'+ str(i)+' to check proxy')
        time.sleep(1)       #保证子线程已经获取数据
    for th in threadpool:
        threading.Thread.join(th)
    print('[INFO] '+'All thread-check-ip have finshed at '+time.ctime())
    cursor = conn.cursor()
    sql = "SELECT COUNT(*) FROM available"
    cursor.execute(sql)
    res = cursor.fetchone()
    print("[INFO] There are {} available proxies at {}".format(res[0],time.ctime()))
    cursor.close()
    conn.close()        #关闭数据库连接

def cycle_check(interval = 30):
    print("[INFO] Open the thread to check ip from table 'available' every {} minutes".format(interval))
    while True:
        time.sleep(interval*60)   #休眠interval*60s
        print("[INFO] Begin to check ip from table 'available' at {}".format(time.ctime()))
        start_check()
        print("[INFO] thread-check-ip is sleeping")