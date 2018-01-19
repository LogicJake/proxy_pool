# Proxy_IP

## todo
* [ ] 多线程验证代理
* [ ] 定时检测ip池，剔除无用ip
* [ ] 多种存储方式（数据库，redis，txt文本）
* [ ] 打包成exe

## 功能介绍
从[西刺免费代理IP](http://www.xicidaili.com/)爬取国内免费代理，验证有效性后建立ip池。目前只支持保存到txt文本中


## 快速开始
clone仓库，根据需要修改配置文件config.json，运行start.py

##config.json参数说明
### storage_mode
####意义
决定存储方式  
####参数说明
1 代表存储到txt文件，文件名"ip.txt"

### check
####意义
爬取到ip后是否检验有效后存入，如果检验，则初始化ip池所需时间较长
####参数说明
1 检验  
0 不检验


###日志
2018.1.19  
添加配置文件config.json
