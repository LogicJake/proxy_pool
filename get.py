# -*- coding: utf-8 -*-
import http.cookiejar
import urllib
from urllib.error import URLError
from bs4 import BeautifulSoup
import pymysql
import time
from common import Global

def get_ip_from_xc():
    opener = urllib.request.build_opener()
    user_agent = r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
    headers = {'User-Agent': user_agent,
               'Connection': 'keep-alive',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Language': 'zh - CN, zh;q = 0.8',
               'Cache-Control': 'max - age = 0',
               }
    get_url = "http://www.xicidaili.com/nt/"
    validIp = []                    #未经检测的ip地址
    try:
        get_request  = urllib.request.Request(get_url, headers=headers)
        get_response = opener.open(get_request)
        soup = BeautifulSoup(get_response, "html.parser")
        trs = soup.findAll('tr')[1:]    #去除第一行的列名
        for tr in trs:
            tdlist=tr.findAll('td')     #获取td
            ip = tdlist[1].string
            port = tdlist[2].string
            dic = {}
            dic['ip'] = ip
            dic['port'] = port
            validIp.append(dic)
    except URLError as e:
        print(e)
        print('[ERROR] Failed to get the data from xicidaili')
    return validIp

def save_to_mysql(validIp,init):
    try:
        conn = pymysql.connect(host=Global.get_value('host'), user=Global.get_value('user'), passwd=Global.get_value('password'), db=Global.get_value('dbname'), port=Global.get_value('port'),charset='utf8')
        cursor = conn.cursor()
        if init:                #初始化
            cursor.execute("DROP TABLE IF EXISTS origin")
            cursor.execute("DROP TABLE IF EXISTS available")
            sql = """CREATE TABLE origin (
                 ID INT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT,
                 IP  CHAR(20) NOT NULL,
                 PORT  INT(20) NOT NULL,
                 UPDATE_TIME int(11) NOT NULL)"""
            cursor.execute(sql)
            sql = "CREATE TABLE available (IP  CHAR(20) NOT NULL,PORT  INT(20) NOT NULL,UPDATE_TIME int(11) NOT NULL,SPEED FLOAT NOT NULL,UNIQUE (IP) )"
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
        if init:
            print("[ERROR] Failed to initialize proxy data")
        else:
            print("[ERROR] Failed to save proxy data")
        return False

def get_ip(init):         #todo：添加多种获取途径
    validIp = get_ip_from_xc()
    return save_to_mysql(validIp,init)