# encoding: utf-8
# @Time : 2022/6/27 10:05
# @Author : Torres-圣君
# @File : run_spider.py
# @Software : PyCharm
import requests
from lxml import etree
from decrypt_fonts import decrypt_font


class DetailedData:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'Cookie': '',
            'Referer': url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44'
        }

    def run(self):
        res = requests.get(url=self.url, headers=self.headers).text
        # 开始解密页面源码
        html = etree.HTML(decrypt_font(res))
        li_list = html.xpath('//div[@class="reviews-items"]/ul/li')
        for li in li_list:
            # 用户昵称
            name = li.xpath('.//a[@class="name"]/text()')[0].strip()
            # 发布日期
            date = li.xpath('.//span[@class="time"]/text()')[0].strip()
            # 评分
            score = '.'.join(li.xpath('.//div[@class="review-rank"]/span[1]/@class')[0].split()[1][-2:])
            # 内容
            comment = ''.join(li.xpath('.//div[contains(@class,"review-words")]/text()')).replace('\n', '').strip()
            item = [name, date, score, comment]
            print(item)


if __name__ == '__main__':
    # 随便拿一家店铺的评论做个测试
    url = 'https://www.dianping.com/shop/H1XZuxIfuHl8meAJ/review_all'
    dd = DetailedData(url)
    dd.run()
