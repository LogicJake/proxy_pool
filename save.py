# -*- coding: utf-8 -*-

def saveIp(choice,validIp):
    if choice == 1:
        saveToTxT(validIp)

def saveToTxT(validIp):
    f = open('ip.txt', 'w', encoding="utf-8")
    for info in validIp:
        ip = info['ip']
        port = info['port']
        f.write(ip + ' ')  # ip
        f.write(port + ' ')  # port
        f.write('\n')
    f.close()