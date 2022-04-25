## <center>✨搭建一个简易的免费IP代理池✨</center>
 - 爬取的免费IP代理的网站包含：
    - [http://www.66ip.cn/index.html](http://www.66ip.cn/index.html)
    - [https://www.89ip.cn/index_1.html](https://www.89ip.cn/index_1.html)
    - [https://ip.ihuan.me/address/5Lit5Zu9.html](https://ip.ihuan.me/address/5Lit5Zu9.html)
    - [https://proxy.ip3366.net/free/?action=china&page=1](https://proxy.ip3366.net/free/?action=china&page=1)
    - [https://ip.jiangxianli.com/blog.html?page=1](https://ip.jiangxianli.com/blog.html?page=1)
    - [https://www.kuaidaili.com/free/inha/1/](https://www.kuaidaili.com/free/inha/1/)

```python
# 运行主方法：ip_pool_run.py 即可启动爬虫

# 该爬虫使用到了threading多线程(没有做到极致，可自行后续优化)，同时对这些网站进行ip代理抓取
# 将所有网站抓取到的ip添加到test_ip方法进行测试，如果代理可用则将其保存至ip_pool.json
```

 - 该程序使用到的模块包含：
     - lxml
     - requests
     - time
     - json
     - random
     - threading
