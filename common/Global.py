# -*- coding: utf-8 -*-

def __init__(): #初始化
    try:
        from common import config
    except ImportError:
        print('[ERROR] Please run in the root directory')
        exit(-1)
    global _global_dict
    _global_dict = {}
    config = config.open_accordant_config("config.json")
    _global_dict['host'] = config['host']
    _global_dict['user'] = config['user']
    _global_dict['password'] = config['password']
    _global_dict['dbname'] = config['dbname']
    _global_dict['port'] = config['port']

def set_value(key,value):
    """ 定义一个全局变量 """
    _global_dict[key] = value


def get_value(key,defValue=None):
    try:
        return _global_dict[key]
    except KeyError:
        return defValue
