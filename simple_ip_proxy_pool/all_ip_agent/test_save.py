# encoding: utf-8
# @Time : 2022/4/23 12:09
# @Author : Torres-圣君
# @File : test_save.py
# @Sofaware : PyCharm
import requests
import json


def test_ip(poxyz):
    url = "http://www.baidu.com"
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.46'
    }
    try:
        res = requests.get(url=url, headers=headers, proxies=poxyz, timeout=2)
        if res.status_code == 200:
            save_ip(poxyz)
    except Exception:
        pass


def save_ip(poxyz):
    data = json.dumps(poxyz, indent=1)
    with open("./ip_pool.json", "a") as w:
        w.write(data+",")
        print(f"<{poxyz}>已写入IP代理池...")
