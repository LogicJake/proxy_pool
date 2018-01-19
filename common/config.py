# coding: utf-8
'''
默认PEP8的docstring，文件注释写在这里
'''
import os
import sys
import json
import re


def open_accordant_config():
    '''
    调用配置文件
    '''
    config_file = sys.path[0]+os.path.sep+"config.json"
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            print("Load config file from {}".format(config_file))
            return json.load(f)
    else:
        print("缺少配置文件")

