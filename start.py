# -*- coding: utf-8 -*-
from get import *
from test import *
from common import Global

if __name__ =="__main__":
    Global.__init__()
    res = get_ip(init=True)
    if res:
        start_test()
