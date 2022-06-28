# encoding: utf-8
# @Time : 2022/6/28 14:50
# @Author : Torres-圣君
# @File : run_spider.py
# @Software : PyCharm
import re
import os
import time
import requests
from selenium import webdriver


class DownloadVideo:
    def __init__(self, url):
        self.url = url
        self.headers = {
            # 记得补充一下自己的cookie值
            "cookie": "",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37"
        }
        # 使用无头模式
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('-–disable-gpu')
        self.driver = webdriver.Chrome(options=options)

    def run(self):
        self.driver.get(self.url)
        # 将滚轮滑到最底部，从而加载所有视频
        # self.move_pulley()
        # 作者昵称
        author_name = self.driver.find_elements_by_xpath('//span[@class="Nu66P_ba"]')[0].text
        print(author_name)
        # 以作者名称创建文件夹
        try:
            os.mkdir(author_name)
        except FileExistsError:
            print(f"{author_name} 文件夹已存在！")
        li_list = self.driver.find_elements_by_xpath('//li[@class="ECMy_Zdt"]')
        for li in li_list:
            video_link = li.find_element_by_xpath('./a').get_attribute('href')
            print("正在保存 --- ", video_link)
            item, video_url = self.get_video_url(video_link)
            self.save_video(item, video_url, author_name)
            time.sleep(3)
            break

    def move_pulley(self):
        temp_height = 0
        while True:
            # 循环将滚动条下拉
            self.driver.execute_script("window.scrollBy(0,500)")
            # sleep一下让滚动条反应一下
            time.sleep(1)
            # 获取当前滚动条距离顶部的距离
            check_height = self.driver.execute_script(
                "return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")
            # 如果两者相等说明到底了
            if check_height == temp_height:
                break
            temp_height = check_height

    def get_video_url(self, video_link):
        res = requests.get(video_link, headers=self.headers).text
        # 对返回的源码进行url解码
        unquote_res = requests.utils.unquote(res)
        # 原视频链接，用于下载保存
        video_url = "https:" + re.findall('"src":"(.*?)"},', unquote_res)[0]
        # 获取视频其他信息
        item = self.get_other_data(unquote_res, video_link)
        return item, video_url

    def get_other_data(self, unquote_res, video_link):
        other_data = re.findall('<span class="CE7XkkTw">(.*?)</span>', unquote_res)
        item = [
            # 视频链接
            video_link,
            # 视频标题
            re.findall('<title.*>(.*?)</title>', unquote_res)[0],
            # 视频点赞数
            other_data[0],
            # 视频评论数
            other_data[1],
            # 视频收藏数
            other_data[2],
            # 视频的发布日期
            re.findall('<span class="aQoncqRg">(.*?)</span>', unquote_res)[0].split('>')[-1]
        ]
        return item

    def save_video(self, item, video_url, author_name):
        with open(f'{author_name}/{item[1]}.mp4', 'wb') as w:
            res = requests.get(video_url).content
            w.write(res)
            print(item[1], " --- 保存完成！")
        with open(f'{author_name}/{author_name}_所有视频信息.csv', 'a+') as a:
            if a.read() == '':
                a.write(f'视频链接,视频标题,点赞数,评论数,收藏数,发布日期\n')
            a.write(','.join(item) + '\n')


if __name__ == '__main__':
    dv = DownloadVideo('https://www.douyin.com/user/MS4wLjABAAAAkvysSgdqmkgtgucxkirpMWFHbTeZgVOW7zcdUjU3jM4')
    dv.run()
