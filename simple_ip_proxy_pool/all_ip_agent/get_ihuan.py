# encoding: utf-8
# @Time : 2022/4/23 10:14
# @Author : Torres-圣君
# @File : get_ihuan.py
# @Sofaware : PyCharm
# https://ip.ihuan.me/address/5Lit5Zu9.html
from user_agent import get_ua
from test_save import test_ip
import time
import requests
from lxml import etree

main_url = "https://ip.ihuan.me/address/5Lit5Zu9.html/"
next_url = ""
headers = {
    "User-Agent": get_ua()
}


def get_data(num):
    global next_url
    next_url = parse(main_url)
    for i in range(1, num+1):
        time.sleep(1)
        parse(next_url)


def parse(url):
    try:
        global next_url
        res = requests.get(url, headers=headers, timeout=2)
        page = etree.HTML(res.text)
        ip_list = page.xpath('//table//tr')
        # print(len(ip_list))
        for i in range(1, len(ip_list)):
            # 提取ip地址
            ip_address = ip_list[i].xpath(f'./td[1]/a/text()')[0]
            # 提取ip端口
            ip_port = ip_list[i].xpath(f'./td[2]/text()')[0]
            # 提取ip类型
            ip_type = ip_list[i].xpath(f'./td[5]/text()')[0]
            if ip_type == "支持":
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
        next_url = main_url + page.xpath('//ul[@class="pagination"]/li[3]/a/@href')[0]
        return next_url
    except IndexError:
        pass
