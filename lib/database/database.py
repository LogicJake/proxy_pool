# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-01-16 13:21:21
# @Last Modified time: 2019-01-22 19:55:42
from abc import ABCMeta, abstractmethod


class DataBase(metaclass=ABCMeta):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def update(self, table_name, key_values, where):
        pass

    @abstractmethod
    def insert(self, table_name, key_values):
        pass

    @abstractmethod
    def is_table_exist(self, table_name):
        pass

    @abstractmethod
    def select(self, table_name, column_name, where=None, limit=None, order_by=None, order='desc'):
        pass

    @abstractmethod
    def delete(self, table_name, where=None):
        pass

    @abstractmethod
    def create_required_tables(self):
        pass
