## <center>✨获取美团美食的店铺信息✨</center>
 - 美团北京美食所有店铺：[https://bj.meituan.com/meishi/](https://bj.meituan.com/meishi/)

```python
修改 'self.start_url' ：修改为想要抓取的城市url
修改 'self.headers' 下的 'Cookie'和'User-Agent'：修改为自己账号登录后的值
修改 'self.mongo_address' ：修改为自己的MongoDB数据库地址
更换 'ip_pool_run.py'：修改其文件下的IP代理地址
```

 - 爬取美团北京美食店铺的信息，包含：
    - 店铺链接
    - 店铺名称
    - 店铺地址
    - 店铺评论数
    - 店铺评分
 - 爬取的数据存储方式：
    - 通过连接MongoDB数据库，将其存入数据库
 - 该爬虫使用到的模块：
	 - requests
	 - re
	 - time
	 - json
	 - pymongo