# -*- coding:utf-8 -*-
# @Time : 2021/11/15 14:06
# @Author : Torres-圣君
# @File : run_spider.py
# @Software : PyCharm
import time
import json
import requests


class HeroMessage:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53",
        }
        self.heroes_message_list = []
        self.error_list = []

    # 获取英雄对应的链接
    def get_heroes_link(self):
        url = "https://yz.lol.qq.com/v1/zh_cn/champion-browse/index.json"
        res = requests.get(url, headers=self.headers).json()
        heroes_list = res["champions"]
        for heroes in heroes_list:
            item = dict()
            # 英雄上线日期
            item['上线日期'] = heroes["release-date"][:10]
            # 英雄英文名称
            item['英文名称'] = heroes["slug"]
            # 英雄信息的链接
            heroes_slug_link = f"https://yz.lol.qq.com/v1/zh_cn/champions/{item['英文名称']}/index.json"
            # 获取英雄详细信息
            try:
                self.heroes_message_list.append(
                    self.get_heroes_msg(heroes_slug_link, item)
                )
            except:
                print(heroes_slug_link, "获取信息失败!")
                self.error_list.append(heroes_slug_link)
            time.sleep(0.5)
        # 保存英雄全部数据
        self.save_data(self.heroes_message_list)
        # 采集失败的链接
        print("采集失败的链接", self.error_list)

    # 获取英雄别名->英雄名全称
    def get_heroes_msg(self, heroes_slug_link, item):
        # 显示正在请求的链接
        print("正在获取：", heroes_slug_link)
        # 对链接发送请求
        res = requests.get(heroes_slug_link, self.headers).json()
        # 英雄中文名称
        item['英雄名称'] = res["champion"]["title"] + "·" + res["champion"]["name"]
        # 英雄定位
        item['英雄定位'] = ", ".join([roles["name"] for roles in res["champion"]["roles"]])
        # 英雄台词
        item['英雄台词'] = res["champion"]["biography"]["quote"].strip("“”").replace("</i>", "")
        # 英雄链接
        item['英雄链接'] = "https://yz.lol.qq.com/zh_CN/champion/" + item['英文名称']
        # 英雄原画
        item['原画链接'] = res["champion"]["image"]["uri"]
        # 英雄精简故事
        item['故事简述'] = res["champion"]["biography"]["short"].strip("</p>")
        # 英雄完整故事
        item['背景故事'] = res["champion"]["biography"]["full"].strip("</p>").replace("</p>", "").replace("</i>", "").replace(r"\n", "")
        # print(item)
        return item

    # 保存英雄数据
    def save_data(self, dict_data):
        data = json.dumps(dict_data, indent=1, ensure_ascii=False)
        with open("heroes_data.json", "w", encoding='utf-8') as w:
            w.write(data)
            print("英雄信息写入完成...")


if __name__ == '__main__':
    hero = HeroMessage()
    hero.get_heroes_link()
