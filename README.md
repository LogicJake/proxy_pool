# Proxy_IP

![pyversions](https://img.shields.io/badge/python%20-3.5%2B-blue.svg)
![Travis](https://img.shields.io/travis/rust-lang/rust.svg)
## todo
* [x] 每隔一段时间爬取免费代理保存到数据库（建立一个origin表）
* [x] 检测origin表的代理有效性，将有效的代理和其访问时间存到available表
* [x] 每隔一段时间检测aviable表，从available表取长时间未被检测的一部分数据检查，剔除无效代理
* [x] 爬取更多代理源

## 功能介绍
从[西刺免费代理IP](http://www.xicidaili.com/)爬取国内免费代理，验证有效性后建立ip池。目前只支持保存到MySQL数据库中。每隔一段时间验证代理池中代理有效性和连接时间。


## 快速开始
clone仓库，修改配置文件config.json，运行start.py文件。

## config.json参数说明
* host：数据库地址，加入在本地，直接填写"localhost"；在远程服务器填写服务器ip地址。
* port：端口地址，默认为3306，一般不需要更改
* user：用户名
* password：密码
* dbname：存储的数据库名称，需要事先创建好

## 日志
2018.1.19  
* 添加配置文件config.json

2018.1.20  
* 支持存储到mysql数据库

2018.1.21  
* 多线程定时检测origin表内数据  
* 多线程定时检测available表代理的有效性和连接时间


2018.1.23
* 更改算法：每次爬取代理后立即启动检测程序，根据少量多次的思想进行检测工作。同时检测线程会每隔10分钟启动检测未验证代理库里是否还有漏网之鱼
* 爬取快代理，快代理免费代理质量不是很高
