# encoding: utf-8
# @Time : 2022/4/16 19:32
# @Author : Torres-圣君
# @File : get_data.py
# @Sofaware : PyCharm
import requests
from .ua_pool import *


class CsdnHot:
    def __init__(self, page_, type_):
        # 页面数据起始的URL
        self.url = f"https://blog.csdn.net/phoenix/web/blog/hot-rank"
        # 自定义请求头
        self.headers = {
            "user-agent": get_user_agent(),
        }
        # 发送请求时需要携带的参数
        self.params = {
            "page": page_,
            "pageSize": 25,
            "child_channel": type_,
            "type": None
        }

    def get_data(self):
        # 创建一个空列表，用于保存所有字典数据
        list_data = []
        # 模拟请求
        res = requests.get(self.url, headers=self.headers, params=self.params)
        # 获取页面返回的数据，并转换为json
        data = res.json()
        for i in range(0, 25):
            # 创建空字典
            item = {}
            # 文章标题
            item["标题"] = data["data"][i]["articleTitle"]
            # 文章作者
            item["作者"] = data["data"][i]["nickName"]
            # 文章链接
            item["链接"] = data["data"][i]["articleDetailUrl"]
            # 文章浏览数
            item["浏览数"] = data["data"][i]["viewCount"]
            # 文章收藏数
            item["收藏数"] = data["data"][i]["commentCount"]
            # 文章评论数
            item["评论数"] = data["data"][i]["favorCount"]
            # 向列表内追加数据
            list_data.append(item)
        # 返回列表数据
        return list_data
