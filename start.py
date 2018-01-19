# -*- coding: utf-8 -*-
from GetIP import GetIP

if __name__ =="__main__":
    try:
        from common import config
    except ImportError:
        print('请在项目根目录中运行脚本')
        exit(-1)
    config = config.open_accordant_config()
    check = config['check']
    save = config['storage_mode']
    GetIP(check=check,save=save)
