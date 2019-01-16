# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-01-16 16:12:15
# @Last Modified time: 2019-01-16 21:03:17
from abc import ABCMeta, abstractmethod


class BasicSource(metaclass=ABCMeta):

    @abstractmethod
    def get_proxy(self):
        pass
