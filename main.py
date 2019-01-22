# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-01-16 11:25:12
# @Last Modified time: 2019-01-22 19:21:05

from config import logger
from lib.database import db_object
import argparse
from get_proxy import GetProxy
from validate import ValidateOrigin
from test import TestAvailable
import threading


def init(db_type):
    db_obj = db_object.new_db(db_type)
    db_obj.connect()
    db_obj.create_required_tables()

    num = db_obj.select('available', ['COUNT(*)'])
    num = num[0][0]
    logger.info('There are {} available proxies'.format(num))
    logger.info('The proxy pool is initialized successfully')
    db_obj.close()


def start(args):
    db_type = args.database
    init(db_type)

    get_proxy = GetProxy(db_type)
    validate_origin = ValidateOrigin(db_type)
    test_available = TestAvailable(db_type)

    thread_get_proxy = threading.Thread(
        target=get_proxy.cycle_get, name="thread-get-ip")  # 定时从网站获取ip
    thread_validate_proxy = threading.Thread(
        target=validate_origin.cycle_validate, name="thread-validate-ip")  # 定时测试能用代理
    thread_test_proxy = threading.Thread(
        target=test_available.cycle_test, name="Thread-test-ip")  # 定时检查，剔除不能用的代理

    thread_get_proxy.start()
    thread_validate_proxy.start()
    thread_test_proxy.start()


def parse_args():
    # Parses arguments
    parser = argparse.ArgumentParser(
        description="collect proxy from internet.")

    parser.add_argument('--database', nargs='?', default='mysql', type=str)

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    start(args)
