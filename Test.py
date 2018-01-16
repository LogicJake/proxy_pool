# -*- coding: utf-8 -*-
import telnetlib
def TestIP(ip,port):
    # 连接Telnet服务器
    try:
        tn = telnetlib.Telnet(ip, port=port, timeout=20)
    except:
        print('失败')
    else:
        print('成功')
