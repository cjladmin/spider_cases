## <center>✨获取汽车之家口碑信息✨</center>
 - 随便拿一条口碑信息做个测试：[https://k.autohome.com.cn/detail/view_01g5ryk7f66gt34d9p6wvg0000.html](https://k.autohome.com.cn/detail/view_01g5ryk7f66gt34d9p6wvg0000.html)

```python
字体反爬大体思路：
    1. 通过口碑页面的源码中，提取'.ttf'字体链接，并保存该字体
    2. 使用'fontTools'模块提取字体中所有的文字编号，后将这些编号和文字建立映射
    3. 建立映射时，需把字体编号的'uni'替换为和源码中相同的'&#x'形式
    4. 最后将页面源码中的加密文字进行替换即可
```

 - 该爬虫使用到的模块：
	 - requests
     - re
     - lxml
     - fontTools
