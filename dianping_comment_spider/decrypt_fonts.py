# encoding: utf-8
# @Time : 2022/6/27 16:56
# @Author : Torres-圣君
# @File : decrypt_fonts.py
# @Software : PyCharm
import requests
import re


def decrypt_font(html):
    print("正在获取css链接！")
    css_link = get_css_link(html)
    print("正在获取svg链接！")
    svg_res, css_res = get_svg_link(css_link)

    # 创建空字典，用于存放'文字css样式的class值'和'文字的坐标值'
    css_dict = {}
    xy_list = re.findall('.(.*?){background:(.*?).0px (.*?).0px;}', css_res)
    for css in xy_list:
        css_dict[css[0]] = (int(css[1]), int(css[2]))

    # 创建空字典，用于存放'id对应的值'和'文字所在的y坐标'
    text_height_dict = {}
    # 提取所有id和y坐标信息
    defs_list = re.findall('<path id="(.*?)" d="M0 (.*?) H600"/>', svg_res)
    for height in defs_list:
        text_height_dict[height[0]] = height[1]

    # 创建空字典，用于存放'文字坐标'和'对应的文字'
    word_dict = {}
    # 提取所有行号、y坐标、行文字
    text_list = re.findall('<textPath xlink:href="#(.*?)" textLength="(.*?)">(.*?)</textPath>', svg_res)
    for row in text_list:
        for word in row[2]:
            # 使用线性回归得出相应公式，从而计算出文字的坐标信息
            word_dict[((row[2].index(word) + 1) * -14 + 14, int(text_height_dict[row[0]]) * -1 + 23)] = word

    # 提取页面源码中加密的文字
    fonts_dic = {f'<svgmtsi class="{i}"></svgmtsi>': word_dict.get(css_dict[i], '*') for i in css_dict}
    # 替换页面源码所有加密文字
    for key in fonts_dic:
        html = html.replace(key, fonts_dic[key])
    return html


def get_css_link(html):
    # 使用re提取css样式链接
    query_css_link = re.findall('href="//s3plus.meituan.net/v1/(.*?)"', html)[0]
    css_link = 'https://s3plus.meituan.net/v1/' + query_css_link
    print(css_link)
    return css_link


def get_svg_link(css_link):
    # 对css链接发送请求，并使用正则提取SVG的链接
    css_res = requests.get(css_link).text
    svg_link = 'https:' + re.findall(r'class\^="qxu".*url\((.*?)\);', css_res)[0]
    print(svg_link)
    # 对SVG链接发送请求，获取其中的文字
    svg_res = requests.get(svg_link).text
    return svg_res, css_res
