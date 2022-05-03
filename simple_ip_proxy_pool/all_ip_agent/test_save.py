# encoding: utf-8
# @Time : 2022/4/23 12:09
# @Author : Torres-圣君
# @File : test_save.py
# @Sofaware : PyCharm
import requests
import json
from user_agent import get_ua


# 测试ip代理是否可用
def test_ip(poxyz):
    url = "http://www.baidu.com"
    headers = {
        "User-Agent": get_ua()
    }
    try:
        res = requests.get(url=url, headers=headers, proxies=poxyz, timeout=1)
        if res.status_code == 200:
            save_ip(poxyz)
    except Exception:
        pass


# 将可用的代理进行保存
def save_ip(poxyz):
    data = json.dumps(poxyz, indent=1)
    with open("./ip_pool.json", "a") as w:
        w.write(data+",")
        print(f"<{poxyz}>已写入IP代理池...")

