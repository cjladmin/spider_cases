# encoding: utf-8
# @Time : 2022/5/11 18:33
# @Author : Torres-圣君
# @File : get_url_data.py
# @Sofaware : PyCharm
import requests
from lxml import etree
from save_data import *


class ExtractData:
    def __init__(self, url):
        self.url = url
        # 需要携带的请求头
        self.headers = {
            "Referer": "https://piaofang.maoyan.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36 Edg/101.0.1210.39"
        }
        self.html = etree.HTML(requests.get(self.url, headers=self.headers).text)

    def who_owns(self):
        # 判断进来的链接，根据不同的链接选用不同的解析方式
        if "box-office" in self.url:
            self.box_office()
        elif "session" in self.url:
            self.session()
        elif "web-heat" in self.url:
            self.web_heat()
        elif "getTVList" in self.url:
            self.getTVList()

    def box_office(self):
        data_list = []
        header_list = ["影片", "票房(万)", "票房占比", "排片占比", "排座占比"]
        data_list.append(header_list)
        for i in range(1, 11):
            body_list = self.html.xpath(f'//*[@class="table-body"]/tr[{i}]')
            for body in body_list:
                item = [
                    body.xpath('./td[1]/div/p[1]/text()')[0],
                    body.xpath('./td[2]/div/text()')[0],
                    body.xpath('./td[3]/div/text()')[0],
                    body.xpath('./td[4]/div/text()')[0],
                    body.xpath('./td[5]/div/text()')[0]
                ]
                data_list.append(item)
        save_data(data_list, "实时票房")

    def session(self):
        data_list = []
        header_list = ["片名", "场次占比", "场次"]
        data_list.append(header_list)
        for i in range(1, 12):
            body_list = self.html.xpath(f'//table//tr[{i}]')
            for body in body_list:
                item = [
                    body.xpath('./td[1]/div/div/span/text()')[0],
                    body.xpath('./td[2]/div/text()')[0],
                    body.xpath('./td[3]/div/text()')[0]
                ]
                data_list.append(item)
        save_data(data_list, "电影排片")

    def web_heat(self):
        data_list = []
        header_list = ["节目", "平台", "上线时长", "实时热度"]
        data_list.append(header_list)
        for i in range(1, 11):
            body_list = self.html.xpath(f'//*[@class="table-body"]/tr[{i}]')
            for body in body_list:
                item = [
                    body.xpath('./td[1]/div/div[2]/p[1]/text()')[0],
                    body.xpath('./td[1]/div/div[2]/p[2]/text()')[0],
                    body.xpath('./td[1]/div/div[2]/p[2]/span/text()')[0],
                    body.xpath('./td[2]/div/div[1]/div[1]/text()')[0]
                ]
                data_list.append(item)
        save_data(data_list, f"影视热度榜")

    def getTVList(self):
        data_list = []
        title = "央视频道" if "0" in self.url else "卫视频道"
        header_list = ["节目", "频道", "实时关注度", "市占率"]
        data_list.append(header_list)
        # 获取返回的JSON数据
        json_data = requests.get(self.url, headers=self.headers).json()
        body_list = json_data["tvList"]["data"]["list"]
        for i in range(0, len(body_list)):
            item = [
                body_list[i]["programmeName"],
                body_list[i]["channelName"],
                body_list[i]["attentionRateDesc"],
                body_list[i]["marketRateDesc"]
            ]
            data_list.append(item)
        save_data(data_list, title)

