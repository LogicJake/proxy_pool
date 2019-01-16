# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-01-16 11:25:12
# @Last Modified time: 2019-01-16 21:04:27

from config import logger
from lib.database import db_object
import argparse
from get_proxy import GetProxy
from test_origin import ValidateOrigin


def init(db_type):
    db_obj = db_object.new_db(db_type)
    db_obj.connect()
    db_obj.create_required_tables()

    num = db_obj.select('available', ['COUNT(*)'])
    num = num[0][0]
    logger.info('There are {} available proxies'.format(num))
    logger.info('The proxy pool is initialized successfully')
    db_obj.close()


def parse_args():
    # Parses arguments

    parser = argparse.ArgumentParser(
        description="collect proxy from internet.")

    parser.add_argument('--database', nargs='?', default='mysql', type=str)

    return parser.parse_args()


if __name__ == '__main__':
    # args = parse_args()
    # db_type = args.database
    db_type = 'mysql'
    init(db_type)
    get_proxy = GetProxy(db_type)
    get_proxy.more_proxy()
    validate_origin = ValidateOrigin(db_type)
    validate_origin.start_test()
