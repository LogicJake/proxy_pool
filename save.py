# -*- coding: utf-8 -*-
import pymysql
import time
def saveIp(choice,validIp,init):
    if choice == 1:
        saveToTxT(validIp)
    elif choice == 2:
        return saveToMysql(validIp,init)

def saveToTxT(validIp):
    f = open('ip.txt', 'w', encoding="utf-8")
    for info in validIp:
        ip = info['ip']
        port = info['port']
        f.write(ip + ' ')  # ip
        f.write(port + ' ')  # port
        f.write('\n')
    f.close()

def saveToMysql(validIp,init):
    try:
        from common import config
    except ImportError as e:
        print(e)
    config = config.open_accordant_config("db.json")        #加载数据库连接信息
    try:
        conn = pymysql.connect(host=config['host'], user=config['user'], passwd=config['password'], db=config['dbname'], port=config['port'],charset='utf8')
        cursor = conn.cursor()
        if init:                #初始化
            cursor.execute("DROP TABLE IF EXISTS origin")
            cursor.execute("DROP TABLE IF EXISTS available")
        sql = """CREATE TABLE origin (
                 IP  CHAR(20) NOT NULL,
                 PORT  INT(20) NOT NULL,
                 UPDATE_TIME int(11) NOT NULL)"""
        cursor.execute(sql)
        for ip in validIp:
            sql = "INSERT INTO origin(IP, PORT, UPDATE_TIME) VALUES (\'"+ip['ip']+'\','+ip['port']+',unix_timestamp()'+')'
            cursor.execute(sql)
        cursor.close()
        conn.close()
        print("[INFO] The proxy pool is initialized successfully")
        return True
    except Exception as e:
        print(e)
        print("[ERROR] Failed to initialize proxy data")
        return False
