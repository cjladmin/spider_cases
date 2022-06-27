# encoding: utf-8
# @Time : 2022/6/25 16:36
# @Author : Torres-圣君
# @File : run_spider.py
# @Software : PyCharm
import requests
from lxml import etree
from decrypt_fonts import decrypt_font, save_fonts_dic
from download_fonts import GetFont


class DetailedData:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    def run(self):
        res = requests.get(self.url, headers=self.headers).text
        # 解密页面的字体加密数据
        page_res = decrypt_font(res)
        html = etree.HTML(page_res)
        # 店名
        title = ''.join(html.xpath('//*[@id="body"]/div/div[1]/span/text()'))
        # 评分
        score = ''.join(html.xpath('//div[@class="brief-info"]/span[1]/@title'))
        # 评价数
        comment = ''.join(html.xpath('//span[@id="reviewCount"]//text()')).replace('条评价 ', '').strip()
        # 人均消费
        price = ''.join(html.xpath('//span[@id="avgPriceTitle"]//text()')).replace('人均:', '').strip()
        # 口味评分
        taste = ''.join(html.xpath('//span[@id="comment_score"]/span[1]//text()')).replace('口味:', '').strip()
        # 环境评分
        environment = ''.join(html.xpath('//span[@id="comment_score"]/span[2]//text()')).replace('环境:', '').strip()
        # 服务评分
        service = ''.join(html.xpath('//span[@id="comment_score"]/span[3]//text()')).replace('服务:', '').strip()
        # 地址
        address = ''.join(html.xpath('//span[@id="address"]//text()')).strip()
        # 电话
        phone = ''.join(html.xpath('//p[@class="expand-info tel"]//text()')).replace('电话：', '').strip()
        # 这里只做演示，直接把提取过程写在列表内返回更好
        item = [title, score, comment, price, taste, environment, service, address, phone]
        print(item)


if __name__ == '__main__':
    # 随便拿一家店铺做个测试
    url = 'https://www.dianping.com/shop/H1XZuxIfuHl8meAJ'
    # 填写自己的cookie值
    headers = {
        'Cookie': '填写自己的cookie值',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44',
    }
    # 下载字体
    GetFont(url, headers).run()
    # 用json格式生成字体映射
    save_fonts_dic()
    # 提取页面数据
    dd = DetailedData(url, headers)
    dd.run()
