# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-01-16 20:16:55
# @Last Modified time: 2019-01-22 19:02:08
from lib.database import db_object
from config import logger
import time
import threading
import requests
import re
lock = threading.Lock()


class TestAvailable():

    def __init__(self, db_type):
        db_obj = db_object.new_db(db_type)
        self.db = db_obj

    def get_ip(self, proxies):
        response = requests.get(
            'http://space.bilibili.com/ajax/member/GetInfo', timeout=5, proxies=proxies)
        ip = re.findall(
            r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", response.text)[0]
        return ip

    def test_proxy(self, ip, port):
        proxies = {'http': str(ip) + ':' + str(port)}
        start = time.time()
        try:
            fake_ip = self.get_ip(proxies)
            if fake_ip == ip:
                cost = time.time() - start
                cost = round(cost, 2)
                return cost
            else:
                return False

        except Exception:
            return False

    def update(self, proxy):
        self.db.connect()
        try:
            for p in proxy:
                id = p.pop('ID')
                if p['SPEED']:
                    self.db.update('available', p, 'ID={}'.format(id))
                else:
                    self.db.delete('available', 'ID={}'.format(id))
        except Exception as e:
            logger.error(str(e))
        self.db.close()

    def test_thread(self):
        num = 10
        while True:
            try:
                lock.acquire()
                if len(self.proxies) == 0:
                    lock.release()
                    break

                proxies = self.proxies[:num]
                self.proxies = self.proxies[num:]
                lock.release()

                update_proxy = []
                for proxy in proxies:
                    res = self.test_proxy(proxy[0], proxy[1])
                    dic = {}
                    dic['ID'] = proxy[2]
                    dic['UPDATE_TIME'] = 'unix_timestamp()'
                    dic['SPEED'] = res
                    update_proxy.append(dic)
                self.update(update_proxy)
            except Exception as e:
                logger.error(str(e))

    def start_test(self):
        self.db.connect()
        self.proxies = self.db.select(
            'available', ['IP', 'PORT', 'ID'],  order_by='UPDATE_TIME', order='asc')
        self.db.close()

        threadpool = []
        for i in range(5):
            th = threading.Thread(
                target=self.test_thread, name='thread-test-proxy-' + str(i))
            threadpool.append(th)
            th.start()
        for th in threadpool:
            threading.Thread.join(th)
        logger.info('All thread-test-proxy have finshed')

    def cycle_test(self):
        interval = 1
        logger.info(
            "Start thread to test proxy from table 'available'")
        while True:
            self.db.connect()
            num = self.db.select('available', ['COUNT(*)'])
            num = num[0][0]
            self.db.close()
            if num != 0:
                logger.info("Begin to test proxy from table 'available'")
                self.start_test()
                logger.info("thread-test-proxy is sleeping")
            time.sleep(interval * 60)


if __name__ == '__main__':
    test_available = TestAvailable('mysql')
    test_available.cycle_test()
