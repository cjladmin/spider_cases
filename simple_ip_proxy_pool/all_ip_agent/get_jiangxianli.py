# encoding: utf-8
# @Time : 2022/4/23 16:33
# @Author : Torres-圣君
# @File : get_jiangxianli.py
# @Sofaware : PyCharm
# https://ip.jiangxianli.com/blog.html?page=1
from user_agent import get_ua
from test_save import test_ip
import time
import requests
from lxml import etree


headers = {
    "User-Agent": get_ua()
}


def get_data(num):
    for i in range(1, num+1, 5):
        url = f"https://ip.jiangxianli.com/blog.html?page={str(int(i/5)+1)}"
        get_page(url)


def get_page(url):
    try:
        res = requests.get(url, headers=headers, timeout=2)
        page = etree.HTML(res.text)
        div_list = page.xpath('//div[@class="contar-wrap"]/div')
        for div in div_list:
            time.sleep(1)
            son_url = div.xpath('./div/h3/a/@href')[0]
            parse(son_url)
    except:
        pass


def parse(son_url):
    try:
        res = requests.get(son_url, headers=headers, timeout=2)
        page = etree.HTML(res.text)
        ip_list = page.xpath('//div[@class="item"]/div/p/text()')
        for i in range(0, len(ip_list)):
            # 去除无用字符，并拼接为ip可用格式
            ip_msg = "http://" + ip_list[i].split("@")[0].strip(" \t\n")
            poxyz = {
                "http": ip_msg
            }
            test_ip(poxyz)
    except IndexError:
        pass
