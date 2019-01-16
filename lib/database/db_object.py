# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-01-16 13:26:41
# @Last Modified time: 2019-01-16 13:47:58
from .mysql import MySqlDB


def new_db(type):
    if type == 'mysql':
        return MySqlDB()
