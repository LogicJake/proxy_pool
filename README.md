![pyversions](https://img.shields.io/badge/python%20-3.5%2B-blue.svg)
![Travis](https://img.shields.io/travis/rust-lang/rust.svg)  
[English](https://github.com/LogicJake/proxy_pool/blob/master/README-EN.md)
## 功能介绍
从西刺免费代理和快代理爬取国内免费代理，验证有效性后建立代理池。目前只支持保存到MySQL数据库中。每隔一段时间验证代理池中代理有效性和连接时间。


## 快速开始
* clone仓库  
* 将db.conf.example重命名为db.conf，修改对应字段值
* python main.py &

### db.conf字段说明
* host：数据库地址，假如在本地，直接填写"localhost"；在远程服务器填写服务器ip地址。
* port：端口地址，默认为3306，一般不需要更改
* user：用户名
* password：密码
* dbname：存储的数据库名称，需要事先创建好

## 可扩展
* 新代理源  
假如想添加新的免费代理源，直接在lib/proxy编写新的爬取类，并继承BasicSource。然后在lib/proxy/all_source.py引入。
* 新数据库存储方式  
假如想添加新的数据库存储方式，直接在lib/database编写新的存储方式类，并继承database类。然后在lib/database/db_object.py仿造mysql返回一个实例。


## 日志
2018.2.5  
* 增加高质量ip181代理
* 数据库操作加锁
* config.json添加字段local_ip

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

2019.1.22  
* 重构代码  
* 删除失效的ip181
