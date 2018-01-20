# -*- coding: utf-8 -*-
from GetIP import *
from Test import *

if __name__ =="__main__":
    try:
        from common import config
    except ImportError:
        print('[ERROR] Please run in the root directory')
        exit(-1)
    config = config.open_accordant_config("config.json")
    save = config['storage_mode']
    res = GetIP(save=save,init=True)
    if res:
        StartTest(10)
