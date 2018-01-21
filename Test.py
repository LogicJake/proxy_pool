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

def start_test(num=10):      #默认一次取10条
    try:
        conn = pymysql.connect(host=Global.get_value('host'), user=Global.get_value('user'), passwd=Global.get_value('password'), db=Global.get_value('dbname'), port=Global.get_value('port'),charset='utf8')
        cursor = conn.cursor()
        sql = "select IP,PORT from origin order by UPDATE_TIME desc limit {}".format(num)
        cursor.execute(sql)
        results = cursor.fetchall()
        sql = "delete from origin where 1=1 order by UPDATE_TIME desc limit {}".format(num)     #删除之前获取的10条记录
        cursor.execute(sql)
        validIp = []  # 成功的代理
        print('[INFO] Start to test proxy')
        for proxy in results:
            res = test_ip(proxy[0],proxy[1])
            if res != False:
                dic = {}
                dic['ip'] = proxy[0]
                dic['port'] = proxy[1]
                dic['speed'] = res
                validIp.append(dic)
        print('[INFO] Successfully get {} proxy'.format(validIp.__len__()))
        save(validIp)
        cursor.close()
        conn.close()
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

def save(validIp):
    try:
        conn = pymysql.connect(host=Global.get_value('host'), user=Global.get_value('user'), passwd=Global.get_value('password'), db=Global.get_value('dbname'), port=Global.get_value('port'),charset='utf8')
        cursor = conn.cursor()
        sql="CREATE TABLE IF NOT EXISTS available (IP  CHAR(20) NOT NULL,PORT  INT(20) NOT NULL,UPDATE_TIME int(11) NOT NULL,SPEED FLOAT NOT NULL,UNIQUE (IP) )"
        cursor.execute(sql)
        for ip in validIp:
            #replace into 保证不会插入重复ip，且已存在该ip时执行更新操作
            sql = "REPLACE INTO available(IP, PORT, UPDATE_TIME,SPEED) VALUES ('" + ip['ip'] + "'," + str(ip['port']) + ",unix_timestamp(),"+str(ip['speed']) + ')'
            cursor.execute(sql)
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(e)
        print("[ERROR] Failed to save effective proxy data")
        return False


