# encoding: utf-8
# @Time : 2022/6/25 14:12
# @Author : Torres-圣君
# @File : download_fonts.py
# @Software : PyCharm
import requests
import re


class GetFont:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    def run(self):
        print("正在获取css链接！")
        css_link = self.get_css_link()
        print(css_link)
        print("正在获取字体链接！")
        font_link_list = self.get_font_link(css_link)
        print(font_link_list)
        self.save_font(font_link_list)

    def get_css_link(self):
        res = requests.get(self.url, headers=self.headers).text
        # 使用正则提取css样式链接
        query_css_link = re.findall('href="//s3plus.meituan.net/v1/(.*?)"', res)[0]
        css_link = "https://s3plus.meituan.net/v1/" + query_css_link
        return css_link

    def get_font_link(self, css_link):
        res = requests.get(css_link).text
        # 使用正则提取字体库的链接
        font_link_list = [
            f"https:{i}" for i in re.findall(r'//s3plus.meituan.net/v1/mss_\w{32}/font/\w{8}.woff', res)
        ]
        return font_link_list

    def save_font(self, font_link_list):
        # 六种不同的字体库，实则有三种是一样的
        tags = ['review', 'hours', 'dishname', 'num', 'address', 'shopdesc']
        for num, link in enumerate(font_link_list):
            woff_data = requests.get(link).content
            # 二进制写入文件，保存字体
            with open(f"./woff/{tags[num]}.woff", 'wb') as w:
                w.write(woff_data)
                print(f"{tags[num]} 字体保存完成！")
