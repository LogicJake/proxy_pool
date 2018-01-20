# -*- coding: utf-8 -*-
import pymysql
def saveIp(choice,validIp):
    if choice == 1:
        saveToTxT(validIp)
    elif choice == 2:
        saveToMysql(validIp)

def saveToTxT(validIp):
    f = open('ip.txt', 'w', encoding="utf-8")
    for info in validIp:
        ip = info['ip']
        port = info['port']
        f.write(ip + ' ')  # ip
        f.write(port + ' ')  # port
        f.write('\n')
    f.close()

def saveToMysql(validIp):
    try:
        from common import config
    except ImportError:
        exit(-1)
    config = config.open_accordant_config("db.json")        #加载数据库连接信息
    try:
        conn = pymysql.connect(host=config['host'], user=config['user'], passwd=config['password'], db=config['dbname'], port=config['port'],charset='utf8')
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS pool")
        sql = """CREATE TABLE pool (
                 ID INT(11) primary key auto_increment,
                 IP  CHAR(20) NOT NULL,
                 PORT  INT(20) NOT NULL,
                 UPDATE_TIME DATETIME NOT NULL)"""
        cursor.execute(sql)
        for ip in validIp:
            sql = "INSERT INTO pool(IP, PORT, UPDATE_TIME) VALUES (\'"+ip['ip']+'\','+ip['port']+',NOW())'
            cursor.execute(sql)
        cursor.close()
        conn.close()
    except Exception:
        print("保存到MySQL失败")
