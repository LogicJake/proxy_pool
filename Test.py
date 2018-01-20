# -*- coding: utf-8 -*-
import telnetlib


def StartTest(ips):
    newIps = []
    for ip in ips:
        res = TestIp(ip['ip'],ip['port'])
        if res == 1:
            newIps.append(ip)
    return newIps

def TestIp(ip,port):
    try:
        tn = telnetlib.Telnet(host=ip, port=port, timeout=5)
    except:
        return 0
    else:
        return 1
