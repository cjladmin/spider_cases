# encoding: utf-8
# @Time : 2022/3/30 21:08
# @Author : Torres-圣君
# @File : mian.py
# @Sofaware : PyCharm
import requests
from .get_proxyz import get_proxies
from .get_ua import get_ua
from pymongo import MongoClient


class CatchYibuBook:
    def __init__(self):
        self.url = f'https://www.epubit.com/pubcloud/content/front/portal/getUbookList'
        # 初始化MongoDB数据库并创建数据库连接
        self.mongo_address = '127.0.0.1'
        self.client = MongoClient(self.mongo_address, 27017)
        self.db = self.client['book']
        self.col = self.db['yibutushu']

    def get_data(self, i):
        headers = {
            'Origin-Domain': 'www.epubit.com',
            'User-Agent': get_ua()
        }
        params = {
            'page': i,
            'row': 20,
            'startPrice': None,
            'endPrice': None,
            'tagId': None,
        }

        res = requests.get(self.url, headers=headers, params=params, proxies=get_proxies())
        data = res.json()
        for i in range(0, 20):
            item = {}
            item['book_name'] = data['data']['records'][i]['name']
            item['book_author'] = data['data']['records'][i]['authors']
            item['book_price'] = data['data']['records'][i]['price']
            item['book_tagNames'] = data['data']['records'][i]['tagNames']
            item['book_link'] = "https://www.epubit.com/bookDetails?id=" + data['data']['records'][0]['code']
            self.col.insert_one(item)
            print(item)

    def run(self, page):
        for i in range(1, page+1):
            # 设置抓取数据的页数
            catch_msg.get_data(i)
        # 断开连接mongo
        self.client.close()


if __name__ == '__main__':
    num = int(input("请输入需要爬取的页数："))
    # 实例化对象
    catch_msg = CatchYibuBook()
    catch_msg.run(num)
