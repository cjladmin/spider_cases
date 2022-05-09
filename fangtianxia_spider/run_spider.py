# encoding: utf-8
# @Time : 2022/4/26 18:38
# @Author : Torres-圣君
# @File : douban_run_spider.py
# @Sofaware : PyCharm
# https://zz.newhouse.fang.com/house/s/
import requests
from lxml import etree
import re
import json
import time
from user_agent import get_ua


def run():
    # 获取总页数
    page_number = get_page_number(first_url)
    for i in range(2, page_number+1):
        time.sleep(1)
        url = f"{first_url}b9{str(i)}/"
        parse_page(url)
        print(f"第<{i}>页数据保存完毕！")


def get_page_number(url):
    global city_name
    res = requests.get(url, headers=headers)
    html = etree.HTML(res.text)
    # 城市名称
    city_name = html.xpath('//ul[@class="tf f12"]/li[2]/a/text()')[0]
    # 提取页码
    page_number = html.xpath('//div[@class="otherpage"]/span[2]/text()')[0]
    return int(re.findall(r"(\d+)", page_number)[0])


def parse_page(url):
    res = requests.get(url, headers=headers)
    html = etree.HTML(res.text)
    div_list = html.xpath('//*[@id="newhouse_loupan_list"]/ul/li/div[1]/div[2]')
    # print(len(div_list))
    all_data_list = []
    for div in div_list:
        try:
            item = dict()
            item["title"] = div.xpath('./div[1]/div[1]/a/text()')[0].strip(" \t\n")
            item["area"] = div.xpath('./div[2]//text()')[-1].strip(" \t\n")
            item["price"] = div.xpath('./div[5]/span/text()')[0].strip(" \t\n")
            try:
                item["price"] = item["price"] + div.xpath('./div[5]/em/text()')[0].strip(" \t\n")
            except IndexError:
                pass
            item["link"] = div.xpath('./div[1]/div[1]/a/@href')[0].strip(" \t\n")
            item["address"] = div.xpath('./div[3]/div/a/@title')[0].strip(" \t\n")
            item["comment"] = div.xpath('./div[1]/div[2]/a/span/text()')[0].strip(" ()\t\n")
            # 展示数据
            print(item)
            all_data_list.append(item)
        except IndexError:
            pass
    save_data(all_data_list)


def save_data(item):
    if len(item) != 0:
        date = time.localtime()
        now_date = time.strftime("%Y-%m-%d %H:%M", date)
        data = json.dumps(item, indent=1, ensure_ascii=False)
        with open(f"./data/{city_name}_数据.json", "a", encoding="utf-8") as w:
            w.write(f'"{now_date}": ' + data + ",\n")


if __name__ == '__main__':
    # 房价首页链接
    first_url = "https://zz.newhouse.fang.com/house/s/"
    # 城市名称
    city_name = ""
    headers = {
        "user-agent": get_ua(),
    }
    run()
