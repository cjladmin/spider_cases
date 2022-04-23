# encoding: utf-8
# @Time : 2022/4/22 16:18
# @Author : Torres-圣君
# @File : ip_pool_run.py
# @Sofaware : PyCharm
import random


def get_ip():
    proxys = [
        {
            "http": "http://211.103.138.117:8000"
        }, {
            "http": "http://183.247.215.218:30001"
        }, {
            "http": "http://221.7.197.248:8000"
        }, {
            "http": "http://39.175.85.225:30001"
        }, {
            "http": "http://39.175.85.225:30001"
        }, {
            "http": "http://123.57.246.163:8118"
        }, {
            "http": "http://120.76.244.188:8080"
        }, {
            "http": "http://58.20.232.245:9091"
        }, {
            "http": "http://203.222.25.57:80"
        }, {
            "http": "http://223.96.90.216:8085"
        }, {
            "http": "http://221.7.197.248:8000"
        }, {
            "http": "http://218.64.84.117:8060"
        }, {
            "http": "http://120.220.220.95:8085"
        },
    ]
    return random.choice(proxys)
