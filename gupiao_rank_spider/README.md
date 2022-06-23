## <center>✨获取东方财富个股人气榜✨</center>
 - 东方财富个股人气榜官网：[http://guba.eastmoney.com/rank/](http://guba.eastmoney.com/rank/)

 - 输入日期、出发地、目的地获取火车票信息，包含：
    - 当前排名
    - 排名较昨日变动
    - 股票代码
    - 股票名称
    - 最新价
    - 涨跌额
    - 涨跌幅
    - 最高价
    - 最低价

```python
通过抓包获取到接口后，发现接口数据为aes加密数据
这里通过拿到关键参数，利用js还原加密的密钥和偏移量

使用Python的第三方模块'Crypto'，对AES的CBC模式进行解密
通过解密后的数据，获取每个不同股票对应的代码
再通过对不同代码进行分析和修改，最终构建完整的params
最后携带上params参数对链接发送请求，后提取关键数据，将其存储到data目录下
```

 - 该爬虫使用到的模块：
	 - requests
	 - time
     - json
     - openpyxl
	 - Crypto
	 - base64
