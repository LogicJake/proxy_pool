# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-01-16 11:29:45
# @Last Modified time: 2019-01-16 13:18:15
import logging
import logging.config
import json
import os


# read conf for log
os.makedirs('log', exist_ok=True)
logging.config.fileConfig("log.conf")
logger = logging.getLogger()
logger.info('Finish loading config for logging')


class DBConf():

    def __init__(self):
        # read conf for dababase
        db_conf = 'db.conf'
        if os.path.exists(db_conf):
            with open(db_conf, 'r') as f:
                self.conf = json.load(f)
                logger.info("Finish loading config for database")
        else:
            logger.error("Fail to load config file from {}".format(db_conf))

    def get_value(self, key, defValue=None):
        try:
            return self.conf[key]
        except KeyError:
            return defValue

db_conf = DBConf()
