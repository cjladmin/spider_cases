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
            "cookie": "douyin.com; odin_tt=1b01bcb8d90716d55f94fd5f6db002e5ece540ab2504c8aad2b5c37e03e4aa5567cc13e046ae77344f381490bc9c1d21d95ebec9daf6865b7c654200790fe6a2; ttcid=c92e805224854c19b5e889b9e383e53777; tt_scid=KhTWnuh3idwWm52BSYmLKO85gjugzBkadfxJGESQL2QipMxm76dP7UA2feWh-SPwad73; ttwid=1%7CmDw1LRv-hGPYqQxDacf59SVVc2wZXfToFhcp93NZ2I4%7C1651748569%7C7ad913b4c829af89cb79aa6a3a718f91601cfb083d2bfdb5678b150f4b0d7ec2; passport_csrf_token=b55d814f0b5a8949554209ce20e7dc2b; passport_csrf_token_default=b55d814f0b5a8949554209ce20e7dc2b; s_v_web_id=verify_l2swgdft_jrNsAzY8_CQFp_4qqo_BFvR_jQUKYZmgJmyr; _tea_utm_cache_1300=undefined; douyin.com; strategyABtestKey=1656377462.724; AB_LOGIN_GUIDE_TIMESTAMP=%221656377462532%22; pwa_guide_count=%223%22; THEME_STAY_TIME=%22299511%22; IS_HIDE_THEME_CHANGE=%221%22; _tea_utm_cache_2018=undefined; __ac_signature=_02B4Z6wo00f01M5iVQgAAIDBRSnO6jsm5TzORlGAAFEnatBh5Ap4ZVHVKmxPfyEsJzRZnSWLQj2BzUaK.eu57.agZqr9HEBFR.Ne-qDV81SKwv5RopUJJt-r71QK.8J35QLYWK3xNxEssDg3bc; __ac_nonce=062bab5b100587fc9da87; msToken=MJe-pQK_3-whoNZhStDkPrundY1m5_VxnD3Fq5r7uqAdQH9UmM6ywGHDvlCusCoLmYD1_5Ck2HQxNLZ2-Q2ITHtLo5LJRfrNXtR_OVNTpmyqAd0Q2kaq5LCLKC5G6aqawA==; home_can_add_dy_2_desktop=%221%22; msToken=9Fg3VeHdJJ4UYgMDCRdukBZyj_ikEd0V_2EzCsQLy-Ddhq2dEBf2SsiF7ksHm2XDaZMZP0WNJWWvYLJL8XcRhor4P6DZuKhJxBz8yJFXHZrp8-DwqAKcSUqc4B5_pZGHOQ==",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37"
        }
        self.driver = webdriver.Chrome()

    def run(self):
        self.driver.get(self.url)
        # 将滚轮滑到最底部，从而加载所有视频
        self.move_pulley()
        # 作者昵称
        author_name = self.driver.find_elements_by_xpath('//span[@class="Nu66P_ba"]')[0].text
        print(author_name)
        # 以作者名称创建文件夹
        os.mkdir(author_name)
        li_list = self.driver.find_elements_by_xpath('//li[@class="ECMy_Zdt"]')
        for li in li_list:
            video_link = li.find_element_by_xpath('./a').get_attribute('href')
            print("正在保存 --- ", video_link)
            video_url, video_title = self.get_video_url(video_link)
            self.save_video(video_url, video_title, author_name)
            time.sleep(3)

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
        query_link = re.findall('"src":"(.*?)"},', unquote_res)[0]
        # 视频链接
        video_url = "https:" + query_link
        # 视频标题
        video_title = re.findall('<title.*>(.*?)</title>', unquote_res)[0]
        return video_url, video_title

    def save_video(self, video_url, video_title, author_name):
        with open(f'{author_name}/{video_title}.mp4', 'wb') as w:
            res = requests.get(video_url).content
            w.write(res)
            print(video_title, " --- 保存完成！")


if __name__ == '__main__':
    dv = DownloadVideo('https://www.douyin.com/user/MS4wLjABAAAAkvysSgdqmkgtgucxkirpMWFHbTeZgVOW7zcdUjU3jM4')
    dv.run()
