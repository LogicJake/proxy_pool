# Proxy_IP

![pyversions](https://img.shields.io/badge/python%20-3.5%2B-blue.svg)
![Travis](https://img.shields.io/travis/rust-lang/rust.svg)
## todo
* [ ] 每隔一段时间爬取免费代理保存到数据库（建立一个origin表）
* [ ] 检测origin表的代理有效性，将有效的代理和其访问时间存到available表
* [ ] 每隔一段时间检测aviable表，从available表取长时间未被检测的一部分数据检查，剔除无效代理
* [ ] 配置squid供使用

## 功能介绍
从[西刺免费代理IP](http://www.xicidaili.com/)爬取国内免费代理，验证有效性后建立ip池。目前只支持保存到txt文本和MySQL数据库中。


## 快速开始
clone仓库，根据需要修改配置文件config.json，运行start.py。如果需要保存到MySQL数据库，需要根据本人数据库情况修改db.json
文件。

## config.json参数说明
* storage_mode：存储方式  
参数说明  
1 代表存储到txt文件，文件名"ip.txt"  
2 代表存储到MySQL数据库，需要修改db.json文件

* check：爬取到ip后是否检验有效后存入，如果检验，则初始化ip池所需时间较长  
参数说明  
1 检验  
0 不检验

## db.json参数说明
* host：数据库地址，加入在本地，直接填写"localhost"；在远程服务器填写服务器ip地址。
* port：端口地址，默认为3306，一般不需要更改
* user：用户名
* password：密码
* dbname：存储的数据库名称，需要事先创建好

## 日志
* 2018.1.19  
添加配置文件config.json

* 2018.1.20  
支持存储到mysql数据库

