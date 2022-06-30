# encoding: utf-8
# @Time : 2022/6/29 21:47
# @Author : Torres-圣君
# @File : run_spider.py
# @Software : PyCharm
import requests
import re
from lxml import etree
from fontTools.ttLib import TTFont

url = "https://k.autohome.com.cn/detail/view_01g5ryk7f66gt34d9p6wvg0000.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37"
}


def run():
    res = decrypt_font()
    html = etree.HTML(res)
    # 随便提取一段内容，只做测试
    content = ''.join(html.xpath('//div[@class="kb-con"]/div[1]/p//text()'))
    print(content)


def decrypt_font():
    page_res = download_font()
    words = "不是门味机控量启六低多排性二灯近光雨问过十无耗油和短级远得右比真中硬八加来三音着孩实好七内更有长四身坐保下地冷外养软高响呢的电很自盘一开小副左里九五档当路手泥公动上只了少空皮大矮坏"
    font = TTFont('font.ttf')
    font_list = font.getGlyphOrder()[1:]
    fonts_dic = {}
    for i, v in enumerate(words):
        num_char = font_list[i].replace("uni", "&#x").lower() + ';'
        fonts_dic[num_char] = v
    for i in fonts_dic:
        if str(i) in page_res:
            page_res = page_res.replace(str(i), fonts_dic[i].replace(';', ''))
    return page_res


def download_font():
    # 获取口碑字体链接
    res = requests.get(url, headers=headers).text
    font_url = re.findall('href="(.*?)\.ttf"', res)[0] + ".ttf"
    print("字体链接：", font_url)
    # 保存该字体
    font_data = requests.get(font_url, headers=headers).content
    with open('font.ttf', 'wb') as w:
        w.write(font_data)
        print("字体保存完成！")
    return res


if __name__ == '__main__':
    run()
