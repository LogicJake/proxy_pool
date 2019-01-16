# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-01-16 18:27:52
# @Last Modified time: 2019-01-16 21:05:39
from lib.database import db_object
from config import logger
import time
import threading
import requests
import re
lock = threading.Lock()


class ValidateOrigin():

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

    def save(self, valid_proxy):
        self.db.connect()
        try:
            for proxy in valid_proxy:
                self.db.insert('available', proxy)
        except Exception as e:
            logger.error(str(e))
        self.db.close()
        thread = threading.current_thread()
        logger.info(thread.getName() +
                    ' Successfully get {} validate proxies'.
                    format(valid_proxy.__len__()))

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

                valid_proxy = []
                for proxy in proxies:
                    res = self.test_proxy(proxy[0], proxy[1])
                    if res:
                        dic = {}
                        dic['IP'] = "'{}'".format(proxy[0])
                        dic['PORT'] = proxy[1]
                        dic['SPEED'] = res
                        dic['UPDATE_TIME'] = 'unix_timestamp()'
                        valid_proxy.append(dic)
                self.save(valid_proxy)
            except Exception as e:
                logger.error(str(e))

    def start_test(self):
        self.db.connect()
        num = self.db.select('origin', ['COUNT(*)'])
        num = num[0][0]
        if num == 0:
            logger.info('No data in origin')
        else:
            self.proxies = self.db.select(
                'origin', ['IP', 'PORT', 'ID'], order_by='UPDATE_TIME')
            for proxy in self.proxies:
                self.db.delete('origin', 'ID={}'.format(proxy[2]))
            self.db.close()

            threadpool = []

            for i in range(5):
                th = threading.Thread(
                    target=self.test_thread, name='thread-test-ip-' + str(i))
                threadpool.append(th)
                logger.info('Start thread-test-proxy-' +
                            str(i) + ' to test proxy')
                th.start()
            for th in threadpool:
                threading.Thread.join(th)
            logger.info('All thread-test-proxy have finshed')

    def cycle_validate(self):
        interval = 10
        logger.info(
            "Start thread to test proxy from table 'origin' every {} minutes".format(interval))
        while True:
            time.sleep(interval * 60)
            self.db.connect()
            num = self.db.select('origin', ['COUNT(*)'])
            num = num[0][0]
            self.db.close()
            if num == 0:
                logger.info(
                    "The 'origin' table is empty. thread-test-proxy continues sleeping")
            else:
                logger.info("Begin to test proxy from table 'origin'")
                self.start_test()
            logger.info("thread-test-proxy is sleeping")


if __name__ == '__main__':
    validate_origin = ValidateOrigin('mysql')
    ip = validate_origin.get_ip()
    print(ip)
