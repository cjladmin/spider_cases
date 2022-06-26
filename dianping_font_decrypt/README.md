## <center>✨获取大众点评商铺详细信息✨</center>
 - 随便拿一家店铺做个测试：[https://www.dianping.com/shop/H1XZuxIfuHl8meAJ](https://www.dianping.com/shop/H1XZuxIfuHl8meAJ)

 - 爬取CSDN所有分类的热榜文章信息，包含：
    - 店名
    - 评分
    - 评价数
    - 人均消费
    - 口味评分
    - 环境评分
    - 服务评分
    - 地址
    - 电话

```python
运行该程序前，需先将程序入口的cookie补充完整
字体反爬大体思路：
    1. 通过店铺页面的源码中，提取字体所在的css文件链接
    2. 在css文件中找到所需字体的链接，通过re正则提取链接，并使用requests将其下载到本地
    3. 在店铺页面源码中查看自己所需数据对应的字体样式，看引入的是那种字体，找到后将其建立映射
    4. 建立映射完成后，就可以复原字体的原内容了，这里可以先将页面源码还原再提取所需的数据，也可先提取所需的数据再将其数据字体还原
注：该方法只适用于获取店铺的详细信息。如果要获取不同分类下的店铺数据，需要修改`download_fonts.py`下的字体列表`tags = ['tagName', 'reviewTag', 'address', 'shopNum']`，并重复步骤3的操作即可
```

 - 该爬虫使用到的模块：
	 - requests 
     - fontTools 
     - json 
     - lxml 
     - re
