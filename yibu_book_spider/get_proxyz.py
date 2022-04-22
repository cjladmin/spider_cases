# encoding: utf-8
# @Time : 2022/4/1 17:00
# @Author : Torres-圣君
# @File : get_proxyz.py
# @Sofaware : PyCharm
import random


def get_proxies():
    proxies_list = [
        {
            "ip_address": "http://39.175.67.28:30001"
        }, {
            "ip_address": "http://101.133.138.238:8118"
        }, {
            "ip_address": "http://58.246.58.150:9002"
        }, {
            "ip_address": "http://112.6.117.178:8085"
        }, {
            "ip_address": "http://221.122.91.74:9401"
        }, {
            "ip_address": "http://58.220.95.116:10122"
        }, {
            "ip_address": "http://58.220.95.32:10174"
        }, {
            "ip_address": "http://220.168.132.43:9015"
        }, {
            "ip_address": "http://112.6.117.135:8085"
        }, {
            "ip_address": "http://183.131.85.16:7302"
        }, {
            "ip_address": "http://223.96.90.216:8085"
        }, {
            "ip_address": "http://120.133.231.92:8000"
        }, {
            "ip_address": "http://58.220.95.35:10174"
        }, {
            "ip_address": "http://47.97.191.179:8018"
        }, {
            "ip_address": "http://58.220.95.116:10122"
        }, {
            "ip_address": "http://221.122.91.64:9401"
        }, {
            "ip_address": "http://123.57.246.163:8118"
        },
    ]
    return random.choice(proxies_list)
