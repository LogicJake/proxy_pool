# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-01-16 18:19:16
# @Last Modified time: 2019-01-16 21:03:43
from .basic_source import BasicSource
import requests
from bs4 import BeautifulSoup
from config import logger
import time


class KuaidailiProxy(BasicSource):

    def get_proxy(self):
        user_agent = r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
        headers = {'User-Agent': user_agent,
                   'Connection': 'keep-alive',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                   'Accept-Language': 'zh-CN,zh;q=0.9',
                   'Cache-Control': 'max - age = 0',
                   }
        validIp = []
        for i in range(1, 3):
            get_url = "https://www.kuaidaili.com/free/inha/{}".format(i)
            try:
                get_response = requests.get(
                    get_url, headers=headers, timeout=10)
                soup = BeautifulSoup(get_response.text, "html.parser")
                trs = soup.findAll('tr')[1:]
                for tr in trs:
                    tdlist = tr.findAll('td')
                    ip = tdlist[0].string
                    port = tdlist[1].string
                    dic = {}
                    dic['IP'] = "'{}'".format(ip)
                    dic['PORT'] = port
                    validIp.append(dic)
            except Exception as e:
                logger.error(e.msg)
                logger.error('Failed to get the data from kuaidaili')
            time.sleep(1)
        return validIp
