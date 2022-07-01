## <center>✨获取自如网房源信息✨</center>
 - 自如网官网：[https://www.ziroom.com/z/](https://www.ziroom.com/z/)

```python
字体反爬大体思路：
    1. 通过自如网页面的源码中，提取房价数字的背景图片链接，并保存图片
    2. 使用'PIL'的'Image'将数字图片和纯黑色图片合并(因为保存的图片背景为透明，pytesseract无法识别)
    3. 合并后会生成'text.png'图片，再使用'pytesseract'进行识别提取数字
    4. 将提取的数字和坐标值(固定的)建立映射，再将数字'position'对应的坐标替换对应的数字即可
```

 - 该爬虫使用到的模块：
	 - requests
     - re
     - time
     - lxml
     - pytesseract
     - PIL
