# encoding: utf-8
# @Time : 2022/5/6 12:03
# @Author : Torres-圣君
# @File : run_spider.py
# @Sofaware : PyCharm
import requests
import time
import re
import json


class LolSkins:
    def __init__(self):
        self.url = "https://apps.game.qq.com/daoju/v3/api/hx/goods/app/v71/GoodsListApp.php?"
        self.headers = {
            "referer": "https://daoju.qq.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32"
        }
        self.params = {
            "view": "biz_cate",
            "page": int,
            "pageSize": 16,
            "orderby": "dtShowBegin",
            "ordertype": "desc",
            "cate": 17,
            "appSource": "pc",
            "plat": 1,
            "output_format": "jsonp",
            "biz": "lol",
            "_": int(time.time() * 1000)
        }

    def get_data(self):
        # 初始化字典
        all_skins_data = dict()
        # 循环请求页面
        for i in range(1, 51):
            # 请求间隔
            time.sleep(1)
            # 参数页码
            self.params['page'] = i
            # 发送请求
            res = requests.get(self.url, headers=self.headers, params=self.params)
            # 提取数据
            skins_list = self.data_format(res.text)
            # 添加进字典
            all_skins_data[f"lol道具城第<{i}>页"] = skins_list
        # 保存数据
        self.save_data(all_skins_data)

    def data_format(self, data):
        # 皮肤名称
        skin_name_list = re.findall(r'"propName":"(.*?)"', data)
        # 皮肤价格
        skin_price_list = re.findall(r'"iDqPrice":"(\d+)"', data)
        # 上架日期
        skin_date_list = re.findall(r'"dtBegin":"(.*?)"', data)

        skins_list = []

        for i in range(0, len(skin_name_list)):
            item = dict()
            item["skin_name"] = str(skin_name_list[i]).encode('utf8').decode('unicode_escape').replace("\\", "")
            item["skin_price"] = skin_price_list[i]
            item["skin_date"] = skin_date_list[i]
            skins_list.append(item)
            # 展示数据
            print(item)

        return skins_list

    def save_data(self, all_skins_data):
        # JSON序列化
        json_data = json.dumps(all_skins_data, indent=1, ensure_ascii=False)
        with open("lol_skins_data.json", "w", encoding="utf-8") as w:
            w.write(json_data)


if __name__ == '__main__':
    lol = LolSkins()
    lol.get_data()
