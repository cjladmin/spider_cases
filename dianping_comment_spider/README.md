## <center>✨获取大众点评店铺评论信息✨</center>
 - 随便拿一家店铺的评论做个测试：[https://www.dianping.com/shop/H1XZuxIfuHl8meAJ/review_all](https://www.dianping.com/shop/H1XZuxIfuHl8meAJ/review_all)

 - 获取大众点评店铺评论信息，包含：
    - 用户昵称
    - 发布日期
    - 评分
    - 内容

```python
运行该程序前，需先将cookie补充完整
字体反爬大体思路：
    1. 通过店铺页面的源码中，提取字体所在的css文件链接
    2. 在css文件中找到所需字体的链接，通过re正则提取SVG的链接
    3. 建立映射：
        1. 根据css样式源码，建立'文字css样式的class值'和'文字的坐标值'的映射
        2. 根据SVG的`path`标签内'id'和'd'属性，建立行号和行高的映射
        3. 根据SVG的`textPath`标签内'href'和'textLength'属性，建立文字坐标和对应的文字的映射
    4. 建立映射完成后，替换页面源码中的所有加密文字，最后提取数据即可
注：与店铺信息的字体反爬不同，该字体反爬只适用于'用户评论中字体的解密'
```

 - 该爬虫使用到的模块：
	 - requests
     - lxml
     - re
