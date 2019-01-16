# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-01-16 16:33:28
# @Last Modified time: 2019-01-16 19:43:40
from . import xici, kuaidaili


def get_all_proxy():
    proxy = []
    # proxy.append(xici.XiciProxy())
    proxy.append(kuaidaili.KuaidailiProxy())
    return proxy
