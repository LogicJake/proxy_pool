# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-01-16 16:14:13
# @Last Modified time: 2019-01-16 21:03:54
from .basic_source import BasicSource
import requests
from bs4 import BeautifulSoup
from config import logger


class XiciProxy(BasicSource):

    def get_proxy(self):
        user_agent = r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
        headers = {'User-Agent': user_agent,
                   'Connection': 'keep-alive',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                   'Accept-Language': 'zh - CN, zh;q = 0.8',
                   'Cache-Control': 'max - age = 0',
                   }
        validIp = []
        urls = ["http://www.xicidaili.com/nn/",
                "http://www.xicidaili.com/nt/",
                "http://www.xicidaili.com/wn/"]

        for url in urls:
            for i in range(1, 3):
                get_url = url + str(i)
                try:
                    get_response = requests.get(
                        get_url, headers=headers, timeout=10)
                    soup = BeautifulSoup(get_response.text, "html.parser")
                    trs = soup.findAll('tr')[1:]  # 去除第一行的列名
                    for tr in trs:
                        tdlist = tr.findAll('td')  # 获取td
                        ip = tdlist[1].string
                        port = tdlist[2].string
                        dic = {}
                        dic['IP'] = "'{}'".format(ip)
                        dic['PORT'] = port
                        validIp.append(dic)
                except Exception as e:
                    logger.error(e.msg)
                    logger.error('Failed to get the data from xicidaili')
        return validIp
