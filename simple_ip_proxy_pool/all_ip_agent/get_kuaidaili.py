# encoding: utf-8
# @Time : 2022/4/23 16:45
# @Author : Torres-圣君
# @File : get_kuaidaili.py
# @Sofaware : PyCharm
# https://www.kuaidaili.com/free/inha/1/
from user_agent import get_ua
from test_save import test_ip
import time
import requests
from lxml import etree


def get_data(num):
    for i in range(1, num+1):
        time.sleep(1)
        url = f"https://www.kuaidaili.com/free/inha/{str(i)}/"
        parse(url)


def parse(url):
    try:
        headers = {
            "User-Agent": get_ua()
        }
        res = requests.get(url, headers=headers, timeout=2)
        page = etree.HTML(res.text)
        ip_list = page.xpath('//table//tr')
        del ip_list[0]
        # print(len(ip_list))
        for i in range(1, len(ip_list)):
            # 提取ip地址
            ip_address = ip_list[i].xpath(f'./td[1]/text()')[0]
            # 提取ip端口
            ip_port = ip_list[i].xpath(f'./td[2]/text()')[0]
            # 去除无用字符，并拼接为ip可用格式
            ip_msg = "http://" + ip_address.strip(" \t\n") + ":" + ip_port.strip(" \t\n")
            poxyz = {
                "http": ip_msg
            }
            test_ip(poxyz)
    except IndexError:
        pass
