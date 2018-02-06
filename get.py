# -*- coding: utf-8 -*-
import http.cookiejar
import requests
from bs4 import BeautifulSoup
import pymysql
import time
from common import Global
from test import *

def get_ip_from_xc():
    user_agent = r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
    headers = {'User-Agent': user_agent,
               'Connection': 'keep-alive',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Language': 'zh - CN, zh;q = 0.8',
               'Cache-Control': 'max - age = 0',
               }
    validIp = []                    #未经检测的ip地址
    urls = ["http://www.xicidaili.com/nn/","http://www.xicidaili.com/nt/","http://www.xicidaili.com/wn/"]
    for url in urls:
        for i in range(1, 3):
            get_url = url+str(i)
            try:
                get_response = requests.get(get_url, headers=headers, timeout=10)
                soup = BeautifulSoup(get_response.text, "html.parser")
                trs = soup.findAll('tr')[1:]  # 去除第一行的列名
                for tr in trs:
                    tdlist = tr.findAll('td')  # 获取td
                    ip = tdlist[1].string
                    port = tdlist[2].string
                    dic = {}
                    dic['ip'] = ip
                    dic['port'] = port
                    validIp.append(dic)
            except Exception as e:
                print(e)
                print('[ERROR] Failed to get the data from xicidaili')
    return validIp

def get_ip_from_kdl():
    user_agent = r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
    headers = {'User-Agent': user_agent,
               'Connection': 'keep-alive',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Cache-Control': 'max - age = 0',
               }
    validIp = []  # 未经检测的ip地址
    for i in range(1, 3):
        get_url = "https://www.kuaidaili.com/free/inha/".format(i)
        try:
            get_response = requests.get(get_url, headers=headers, timeout=10)
            soup = BeautifulSoup(get_response.text, "html.parser")
            trs = soup.findAll('tr')[1:]  # 去除第一行的列名
            for tr in trs:
                tdlist = tr.findAll('td')  # 获取td
                ip = tdlist[0].string
                port = tdlist[1].string
                dic = {}
                dic['ip'] = ip
                dic['port'] = port
                validIp.append(dic)
        except Exception as e:
            print(e)
            print('[ERROR] Failed to get the data from kuaidaili')
        time.sleep(1)  # 延时反爬
    return validIp

def get_ip_from_ip181():
    user_agent = r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
    headers = {'User-Agent': user_agent,
               'Connection': 'keep-alive',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Cache-Control': 'max - age = 0',
               }
    validIp = []  # 未经检测的ip地址
    get_url = "http://www.ip181.com"
    try:
        get_response = requests.get(get_url, headers=headers, timeout=10)
        soup = BeautifulSoup(get_response.text, "html.parser")
        trs = soup.findAll('tr')[1:]  # 去除第一行的列名
        for tr in trs:
            tdlist = tr.findAll('td')  # 获取td
            ip = tdlist[0].string
            port = tdlist[1].string
            dic = {}
            dic['ip'] = ip
            dic['port'] = port
            validIp.append(dic)
    except Exception as e:
        print(e)
        print('[ERROR] Failed to get the data from ip181')
    time.sleep(1)  # 延时反爬
    return validIp

def save_to_mysql(validIp):
    try:
        conn = pymysql.connect(host=Global.get_value('host'), user=Global.get_value('user'), passwd=Global.get_value('password'), db=Global.get_value('dbname'), port=Global.get_value('port'),charset='utf8',autocommit = True)
        cursor = conn.cursor()
        for ip in validIp:
            sql = "INSERT INTO origin(IP, PORT, UPDATE_TIME) VALUES ('{}',{},unix_timestamp())".format(ip['ip'],ip['port'])
            cursor.execute(sql)
        cursor.close()
        conn.close()
    except Exception as e:
        print(e)
        print("[ERROR] Failed to save proxy data")

def get_ip():         #todo：添加多种获取途径
    validIp = []
    validIp = validIp + get_ip_from_ip181()
    validIp = validIp + get_ip_from_xc()
    validIp = validIp + get_ip_from_kdl()
    save_to_mysql(validIp)
    start_test()

def cycle_get(interval = 10):
    print("[INFO] Open the thread to get ip from the network every {} minutes".format(interval))
    while True:
        time.sleep(interval*60)   #休眠interval*60s
        print("[INFO] Begin to get ip from the network at {}".format(time.ctime()))
        get_ip()
        print("[INFO] thread-get-ip is sleeping")