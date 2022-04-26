## <center>✨爬取房天下全部的楼盘数据✨</center>
 - 郑州房天下官网：[https://zz.newhouse.fang.com/house/s/](https://zz.newhouse.fang.com/house/s/)

 - 爬取房天下全部的楼盘数据，包含：
    - 楼盘标签
    - 楼盘面积
    - 楼盘价格(平方米)
    - 楼盘的网页链接
    - 楼盘所在地址
    - 楼盘评论数
 - 爬取的数据存储方式：
    - 通过a追加内容模式，将爬取的数据存储到`data/`文件夹下的json文件
 - 该爬虫使用到的模块：
	 - requests
	 - time
	 - json
	 - lxml
	 - re
