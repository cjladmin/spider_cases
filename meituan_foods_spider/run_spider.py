# encoding: utf-8
# @Time : 2022/4/22 14:59
# @Author : Torres-圣君
# @File : douban_run_spider.py
# @Sofaware : PyCharm
import json
import re
import time
from pymongo import MongoClient
import requests
from .ip_pool import get_ip


class MeituanSpider:
    def __init__(self):
        # 目标网址，修改为想要抓取的城市url
        self.start_url = 'https://bj.meituan.com/meishi/'
        # 首先需要登录自己的账号上 获取登录后的Cookie信息和User-Agent来构造响应头
        self.headers = {
            # 修改成自己的cookie
            "Cookie": "uuid=fc13f93e2548beaced.1650610445.1.0.0; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=180500c9c6694-0455eeafa4c762-6b3e555b-144000-180500c9c67c8; ci=1; rvct=1; __mta=147677064.1650610453704.1650610453704.1650610453704.1; client-id=19be5210-8e89-4598-a6e2-0decd5081934; mtcdn=K; userTicket=FZodTvVmqRNBtcSIIGENmCRtUCXxFFlvvDUNbDQC; _yoda_verify_resp=lw%2FRe7KjJCSrXlzZjUUHoMC6cv33iCr7LluQL36vp7W%2FSWLD%2FcLgW2NnaEO1MT8u%2Fy0OGm3szpTRomNQj%2BLkD7AlVDDto75c16MkwWz2LQd39H2TWG5%2Fl6%2Bm5UU7W6F23%2BKoK3jYjHETueVKU67hIe%2Boztzp5vFoGPn3Ygs27T9M9Zf6Pd4zsLPyeFy9452ATZNT%2FFQkbqNOM1BLiHC4CdOT4QhO0DAhJU%2BIGJvnXZrRtPnlhlUulQoUsSJBtGPYwAQFJHOyRRM8CD0GXrMddMsXQiS%2FB8kx6aQFCxZPfFy04QHF26N2ztzmTL30e9Uy4Pqk3hS9w2oMRBsdH0wtTV8Mw1p9eqMAIpjTbuIcedfEt6fr2iQusiMwjUCCWTtt; _yoda_verify_rid=150ee0f22540000c; u=2988513400; n=Torres%E5%9C%A3%E5%90%9B; lt=Oj3P9g2z0stfWgMheCCf9Mw0CLUAAAAAfhEAALOaHf0lOvfBhE0OvVWmFtRqPsSY-1C5Fe7PsvPzZYt-ZYb_cDgiVVNJOFOhMF1fZQ; mt_c_token=Oj3P9g2z0stfWgMheCCf9Mw0CLUAAAAAfhEAALOaHf0lOvfBhE0OvVWmFtRqPsSY-1C5Fe7PsvPzZYt-ZYb_cDgiVVNJOFOhMF1fZQ; token=Oj3P9g2z0stfWgMheCCf9Mw0CLUAAAAAfhEAALOaHf0lOvfBhE0OvVWmFtRqPsSY-1C5Fe7PsvPzZYt-ZYb_cDgiVVNJOFOhMF1fZQ; token2=Oj3P9g2z0stfWgMheCCf9Mw0CLUAAAAAfhEAALOaHf0lOvfBhE0OvVWmFtRqPsSY-1C5Fe7PsvPzZYt-ZYb_cDgiVVNJOFOhMF1fZQ; unc=Torres%E5%9C%A3%E5%90%9B; _lxsdk=180500c9c6694-0455eeafa4c762-6b3e555b-144000-180500c9c67c8; _hc.v=89028ea2-f5ad-36f8-2732-5d938ae5b422.1650611594; lat=39.983375; lng=116.410765; firstTime=1650612012131; _lxsdk_s=180500c9c67-e43-f4b-d35%7C%7C77",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
        }
        # 初始化MongoDB数据库并创建数据库连接
        self.mongo_address = '127.0.0.1'
        self.client = MongoClient(self.mongo_address, 27017)
        self.db = self.client['meituan']
        self.col = self.db['bj_foods']

    # 获取需要爬取的url列表
    def get_url_list(self, url, total_nums):
        url_temp = url + 'pn{}/'
        # 每一页显示显示15个美食  通过获取到每个分类下的总美食数来求出总页数
        pages = total_nums // 15 + 1 if total_nums % 15 != 0 else total_nums // 15
        url_list = [url_temp.format(i) for i in range(1, pages + 1)]
        return url_list

    # 对url进行请求并返回处理后的响应信息
    def parse_url(self, url):
        # self.headers['Cookie'] = random.choice(self.cookies)
        time.sleep(1)
        rest = requests.get(url, headers=self.headers, proxies=get_ip())
        html_str = re.findall(r'window._appState = (.*?);</script>', rest.content.decode())[0]
        return html_str

    # 访问店家详细页面，获取地址和电话
    def get_son_msg(self, url):
        time.sleep(1)
        res = requests.get(url, headers=self.headers, proxies=get_ip())
        # 地址
        address = re.findall(r'"address":"(.*?)",', res.text)[0]
        # 电话
        phone_number = re.findall(r'"phone":"(.*?)",', res.text)[0]
        return address, phone_number

    # 创建item并进行存储
    def get_content_list(self, html_str):
        json_html = json.loads(html_str)
        foods = json_html['poiLists']['poiInfos']
        for i in foods:
            item = {}
            # 获取子链接
            food_id = i['poiId']
            item['链接'] = "https://www.meituan.com/meishi/{}/".format(food_id)
            item['店名'] = i['title']
            item['地址'], item["电话"] = self.get_son_msg(item['链接'])
            item['评论数'] = i['allCommentNum']
            item['评分'] = i['avgScore']
            # item['价格'] = i['avgPrice']
            self.save(item)

    # 保存数据到mongodb数据库中
    def save(self, item):
        # 转换为字典
        data = dict(item)
        # 展示数据
        print(data)
        # 写入数据
        self.col.insert_one(data)

    # 主方法
    def run(self):
        # 首先请求入口url来获取每一个美食分类的url地址
        html_str = requests.get(self.start_url, headers=self.headers, proxies=get_ip())
        str_html = re.findall(r'window._appState = (.*?);</script>', html_str.content.decode())[0]
        json_html = json.loads(str_html)
        # 获取分类链接列表
        cate_list = json_html['filters']['cates'][1:]
        print(cate_list)
        item_list = []

        # 对每一个分类进行分组分别获取美食的分类名和美食的分类的url
        for i in cate_list:
            item = {}
            # 分类的url进行反爬处理，将http替换成https
            # cate_url= i.xpath('./a/@href')[0]
            cate_url = i['url']
            item['cate_url'] = cate_url.replace('http', 'https')
            # item['cate_name'] = i.xpath('./a/text()')[0]
            item['name'] = i['name']
            item_list.append(item)

        # 对每一个美食分类的分类名和分类url地址进行遍历并分别进行处理
        for i in item_list:
            time.sleep(2)
            # https请求
            rest = requests.get(i['cate_url'], headers=self.headers, proxies=get_ip())
            # http替换成https后的全部分类链接
            str_html = re.findall(r'window._appState = (.*?);</script>', rest.content.decode())[0]
            json_html = json.loads(str_html)
            total_nums = json_html['poiLists']['totalCounts']
            # 获取每一页的链接
            url_list = self.get_url_list(i['cate_url'], total_nums)
            for url in url_list:
                time.sleep(2)
                list_html = self.parse_url(url)
                self.get_content_list(list_html)


if __name__ == '__main__':
    meituan = MeituanSpider()
    meituan.run()

