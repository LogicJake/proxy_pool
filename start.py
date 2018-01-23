# -*- coding: utf-8 -*-
from get import *
from test import *
from check import *
from common import Global
import pymysql
import threading

def init():
    Global.__init__()
    conn = pymysql.connect(host=Global.get_value('host'), user=Global.get_value('user'),
                           passwd=Global.get_value('password'), db=Global.get_value('dbname'),
                           port=Global.get_value('port'), charset='utf8')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS origin")
    cursor.execute("DROP TABLE IF EXISTS available")
    sql = "CREATE TABLE origin (ID INT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT,IP  CHAR(20) NOT NULL,PORT  INT(20) NOT NULL,UPDATE_TIME int(11) NOT NULL)"
    cursor.execute(sql)
    sql = "CREATE TABLE available (ID INT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT,IP  CHAR(20) NOT NULL,PORT  INT(20) NOT NULL,UPDATE_TIME int(11) NOT NULL,SPEED FLOAT NOT NULL,UNIQUE (IP),STATUS int(1) NOT NULL DEFAULT 0)"
    cursor.execute(sql)
    print("[INFO] The database is already ")
    get_ip()
    print("[INFO] The proxy pool is initialized successfully")
    sql = "SELECT COUNT(*) FROM available"
    cursor.execute(sql)
    res = cursor.fetchone()
    print("[INFO] There are {} available proxies".format(res[0]))
    cursor.close()
    conn.close()

if __name__ =="__main__":
    init()
    thread_get_ip = threading.Thread(target=cycle_get,name="thread-get-ip")         #定时从网站获取ip
    thread_test_ip = threading.Thread(target=cycle_test, name="thread-test-ip")     #定时测试能用代理
    thread_check_ip = threading.Thread(target=cycle_check, name="Thread-check-ip")  #定时检查，剔除不能用的代理
    thread_get_ip.start()
    thread_test_ip.start()
    thread_check_ip.start()
