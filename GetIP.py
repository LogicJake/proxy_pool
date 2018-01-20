# -*- coding: utf-8 -*-
import http.cookiejar
import urllib
from urllib.error import URLError
from bs4 import BeautifulSoup
from save import saveIp

def GetIPFromxc():
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

def GetIP(save,init):         #todo：添加多种获取途径
    validIp = GetIPFromxc()
    return saveIp(save,validIp,init)