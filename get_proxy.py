# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-01-16 16:18:05
# @Last Modified time: 2019-01-16 20:31:21
from lib.database import db_object
from lib.proxy import all_source
from config import logger
import time


class GetProxy():

    def __init__(self, db_type):
        db_obj = db_object.new_db(db_type)
        self.db = db_obj

    def save(self, proxies):
        self.db.connect()
        try:
            for proxy in proxies:
                proxy['UPDATE_TIME'] = 'unix_timestamp()'
                self.db.insert('origin', proxy)
        except Exception as e:
            logger.error(str(e))
            logger.error('Failed to save proxy data')
        self.db.close()

    def more_proxy(self):
        proxies = []

        proxy_objects = all_source.get_all_proxy()
        for ob in proxy_objects:
            proxies = proxies + ob.get_proxy()

        self.save(proxies)

    def cycle_get(self):
        interval = 10
        logger.info('Start thread to get proxy from network every {} minutes'.format(
            interval))
        while True:
            logger.info('Begin to get proxy from network')
            self.more_proxy()
            logger.info("thread-get-proxy is sleeping")
            time.sleep(interval * 60)
