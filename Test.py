# -*- coding: utf-8 -*-
import telnetlib
def TestIP(ip,port):
    # 连接Telnet服务器
    try:
        tn = telnetlib.Telnet(ip, port=port, timeout=5)
    except:
        return 0
    else:
        return 1
