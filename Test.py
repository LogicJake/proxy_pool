# -*- coding: utf-8 -*-
import time
import requests
import pymysql
'''
首先从origin表中取10条数据进行测试，并将其从origin删除
测试10条代理的可用性和连接速度并存入aviable表
'''

def StartTest(num=10):      #默认一次取10条
    try:
        from common import config
    except ImportError as e:
        print(e)
    config = config.open_accordant_config("db.json")        #加载数据库连接信息
    try:
        conn = pymysql.connect(host=config['host'], user=config['user'], passwd=config['password'], db=config['dbname'], port=config['port'],charset='utf8')
        cursor = conn.cursor()
        sql = "select IP,PORT from origin order by UPDATE_TIME desc limit {}".format(num)
        cursor.execute(sql)
        results = cursor.fetchall()
        sql = "delete from origin where 1=1 order by UPDATE_TIME desc limit {}".format(num)     #删除之前获取的10条记录
        cursor.execute(sql)
        validIp = []  # 成功的代理
        # for proxy in results:
        #     res = TestIp(proxy[0],proxy[1])
        #     if res != False:
        #         dic = {}
        #         dic['ip'] = proxy[0]
        #         dic['port'] = proxy[1]
        #         dic['speed'] = res
        #         validIp.append(dic)
        save(validIp)
        cursor.close()
        conn.close()
    except Exception as e:
        print(e)

def TestIp(ip,port):
    proxies = {'http': str(ip)+":"+str(port)}
    start = time.time()
    try:
        requests.get('http://www.baidu.com',timeout=20,proxies=proxies)
        print('[INFO] Successfully get one proxy')
        cost = time.time() - start
        return cost
    except Exception as e:
        return False

def save(validIp):
    try:
        from common import config
    except ImportError as e:
        print(e)
    config = config.open_accordant_config("db.json")        #加载数据库连接信息
    try:
        conn = pymysql.connect(host=config['host'], user=config['user'], passwd=config['password'], db=config['dbname'], port=config['port'],charset='utf8')
        cursor = conn.cursor()
        sql="CREATE TABLE IF NOT EXISTS available (IP  CHAR(20) NOT NULL,PORT  INT(20) NOT NULL,UPDATE_TIME int(11) NOT NULL,SPEED CHAR(20) NOT NULL) "
        cursor.execute(sql)
        # print(res)
        # sql = """CREATE TABLE origin (
        #          IP  CHAR(20) NOT NULL,
        #          PORT  INT(20) NOT NULL,
        #          UPDATE_TIME int(11) NOT NULL)"""
        # cursor.execute(sql)
        # for ip in validIp:
        #     sql = "INSERT INTO origin(IP, PORT, UPDATE_TIME) VALUES (\'"+ip['ip']+'\','+ip['port']+',unix_timestamp()'+')'
        #     cursor.execute(sql)
        cursor.close()
        conn.close()
        # print("[INFO] The proxy pool is initialized successfully")
        # return True
    except Exception as e:
        print(e)
        print("[ERROR] Failed to initialize proxy data")
        return False


