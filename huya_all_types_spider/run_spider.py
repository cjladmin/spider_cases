# encoding: utf-8
# @Time : 2022/5/18 17:36
# @Author : Torres-圣君
# @File : download_fonts.py
# @Sofaware : PyCharm
# https://www.huya.com/g         全部分类链接
import threading
import requests
import json
import time
from lxml import etree
from get_types_user_msg import NowLiveUsers


class HuyaAllTypes:
    def __init__(self):
        self.url = "https://www.huya.com/g"
        self.headers = {
            "Host": "www.huya.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47"
        }

    def get_types_url(self):
        # 请求目标网站，并将GBK的'\xa0'转为对应的空格
        res = requests.get(self.url, headers=self.headers).text.replace(u'\xa0', u' ')
        html = etree.HTML(res)
        all_links_list = html.xpath('//*[@id="js-game-list"]/li')
        print("共发现%d种分类" % len(all_links_list))
        # 创建字典，用于存放所有数据
        all_types_msg = dict()
        # 循环获取所有分类信息
        for all_links in all_links_list:
            # 字典的存放格式 --> {分类的名称 ：[分类的链接, 分类的gameId]}
            all_types_msg[all_links.xpath('./a/p/text()')[0]] = [
                all_links.xpath('./a/@href')[0],
                all_links.xpath('./a/img/@src')[0].split('/')[-1].split('-')[0]
            ]
        # 将分类信息保存到本地
        self.save_all_types(all_types_msg)
        return all_types_msg

    def save_all_types(self, all_types_msg):
        json_data = json.dumps(all_types_msg, indent=1, ensure_ascii=False)
        # 将分类信息写入JSON文件
        with open('./data/all_types_msg.json', 'w') as w:
            w.write(json_data)
        print("\n全部分类信息保存完毕！")


if __name__ == '__main__':
    # 获取所有分类的链接
    huya = HuyaAllTypes()
    all_types_dict_msg = huya.get_types_url()
    # 获取每个分类下的所有直播用户
    tasks = []
    for key, val in all_types_dict_msg.items():
        users_msg = NowLiveUsers(key, val[0], val[1])
        tasks.append(
            threading.Thread(target=users_msg.get_page_msg)
        )
        # users_msg = NowLiveUsers(key, val[0], val[1])
        # users_msg.get_page_msg()
    for task in tasks:
        # 还是设置间隔1秒比较好点
        time.sleep(1)
        task.start()
    for task in tasks:
        task.join()
