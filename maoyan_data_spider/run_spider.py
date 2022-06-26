# encoding: utf-8
# @Time : 2022/5/11 10:52
# @Author : Torres-圣君
# @File : download_fonts.py
# @Sofaware : PyCharm
import time
from get_url_data import *


class MaoyanData:
    def __init__(self, son_url_list: list):
        self.son_url_list = son_url_list

    def get_data(self):
        for i in self.son_url_list:
            for j in i:
                url = "https://piaofang.maoyan.com/" + j
                print(f"正在获取<{url}>")
                ExtractData(url).who_owns()
                time.sleep(1)


if __name__ == '__main__':
    maoyan = MaoyanData(
        [
            ["box-office?ver=normal"],
            ["session"],
            ["web-heat"],
            ["getTVList?showDate=2&type=" + str(i) for i in range(2)]
        ]
    )
    maoyan.get_data()
