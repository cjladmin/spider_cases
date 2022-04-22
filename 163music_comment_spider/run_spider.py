# encoding: utf-8
# @Time : 2022/4/18 23:21
# @Author : Torres-圣君
# @File : get_page_data.py
# @Sofaware : PyCharm
from selenium import webdriver
import requests
import json


def get_data(music_id):
    web = webdriver.Edge()
    web.get(f"https://music.163.com/#/song?id={music_id}")
    # 等待网页加载完成，不是死等；加载完成即可
    web.implicitly_wait(10)
    # 定位iframe
    iframe = web.find_element_by_css_selector('.g-iframe')
    # 先进入到iframe
    web.switch_to.frame(iframe)
    # 获取歌名
    title = web.find_element_by_css_selector('.tit em').text
    # 获取评论列表
    div_list = web.find_elements_by_css_selector('.itm')
    for i in range(0, len(div_list)-20):
        item = {}
        item["用户名"] = div_list[i].find_element_by_css_selector('.s-fc7').text
        item["评论日期"] = div_list[i].find_element_by_css_selector('.time.s-fc4').text
        item["评论赞数"] = div_list[i].find_element_by_css_selector('.rp').text.split("(")[-1].split(")")[0]
        item["评论内容"] = div_list[i].find_element_by_css_selector('.cnt.f-brk').text.split("：")[-1].replace("\n", " ")
        save_data(title, item)
    web.close()
    print("该歌曲热评已保存完毕!")


def save_data(title, item):
    data = json.dumps(item, indent=1, ensure_ascii=False)
    with open(f"data/{title}_热评.json", "a", encoding="utf-8") as w:
        w.write(data)


def get_music_id(music_name):
    url = f"http://music.163.com/api/search/get/?s={music_name}&limit=1&type=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44"
    }
    res = requests.get(url, headers=headers, )
    music_id = res.json()
    return music_id["result"]["songs"][0]["id"]


if __name__ == '__main__':
    music = input("请输入歌曲ID或名称：")
    if (len(music) == 10) and music.isdigit():
        get_data(music)
    else:
        music = get_music_id(music)
        print("该歌曲的ID为：", music)
        get_data(music)
