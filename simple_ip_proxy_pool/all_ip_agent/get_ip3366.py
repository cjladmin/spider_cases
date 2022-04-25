# encoding: utf-8
# @Time : 2022/4/23 10:12
# @Author : Torres-圣君
# @File : get_ip3366.py
# @Sofaware : PyCharm
# https://proxy.ip3366.net/free/?action=china&page=1
from user_agent import get_ua
from test_save import test_ip
import time
import requests
from lxml import etree


def get_data(num):
    for i in range(1, num+1):
        time.sleep(1)
        url = f"https://proxy.ip3366.net/free/?action=china&page={str(i)}"
        parse(url)


def parse(url):
    try:
        headers = {
            "User-Agent": get_ua()
        }
        res = requests.get(url, headers=headers, timeout=2)
        page = etree.HTML(res.text)
        ip_list = page.xpath('//*[@id="content"]/section/div[2]/table//tr')
        del ip_list[0]
        # print(len(ip_list))
        for i in range(1, len(ip_list)):
            # 提取ip地址
            ip_address = ip_list[i].xpath(f'./td[1]/text()')[0]
            # 提取ip端口
            ip_port = ip_list[i].xpath(f'./td[2]/text()')[0]
            # 提取ip类型
            ip_type = ip_list[i].xpath(f'./td[4]/text()')[0]
            if ip_type == "HTTPS":
                # 去除无用字符，并拼接为ip可用格式
                ip_msg = "https://" + ip_address.strip(" \t\n") + ":" + ip_port.strip(" \t\n")
                poxyz = {
                    "https": ip_msg
                }
            else:
                # 去除无用字符，并拼接为ip可用格式
                ip_msg = "http://" + ip_address.strip(" \t\n") + ":" + ip_port.strip(" \t\n")
                poxyz = {
                    "http": ip_msg
                }
            test_ip(poxyz)
    except IndexError:
        pass
