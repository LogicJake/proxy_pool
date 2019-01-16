# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-01-16 13:21:21
# @Last Modified time: 2019-01-16 17:18:23
from abc import ABCMeta, abstractmethod


class DataBase(metaclass=ABCMeta):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def is_table_exist(self):
        pass

    @abstractmethod
    def select(self):
        pass

    @abstractmethod
    def create_required_tables(self):
        pass

    @abstractmethod
    def close(self):
        pass
