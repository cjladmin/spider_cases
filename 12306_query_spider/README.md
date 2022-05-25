## <center>✨查询12306火车票信息✨</center>
 - 12306官网：[https://www.12306.cn/index/](https://www.12306.cn/index/)

 - 输入日期、出发地、目的地获取火车票信息，包含：
    - 车次
    - 出发时间
    - 到达时间
    - 历时
    - 商务座
    - 一等座
    - 二等座
    - 软卧 
    - 硬卧 
    - 硬座 
    - 无座 
    - 备注

 - 因12306有反爬机制，所以当查询失败时，请更换`cookie`的值后重试
     - 当然也可使用`selenium`自动获取`cookie`，这里则不再演示

 - 该爬虫使用到的模块：
	 - requests
	 - json
	 - openpyxl
	 - prettytable
