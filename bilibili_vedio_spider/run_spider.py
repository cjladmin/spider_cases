# encoding: utf-8
# @Time : 2022/5/9 12:16
# @Author : Torres-圣君
# @File : run_spider.py
# @Sofaware : PyCharm
import requests
import re
import json
import subprocess
import os


class DownloadVideo:
    def __init__(self, url_list: list):
        self.task_url = url_list
        self.headers = {
            "Referer": "https://www.bilibili.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36 Edg/101.0.1210.39",
        }

    def run(self):
        for task in self.task_url:
            if "https://www.bilibili.com/video/" in task:
                url = task
            else:
                url = "https://www.bilibili.com/video/" + task
            res = requests.get(url, headers=self.headers)
            print(f"正在提取{url}...")
            self.format_data(res.text)

    def format_data(self, text_data):
        print("正在提取视频数据 > > >")
        video_title = re.findall(r'<h1 id="video-title" title="(.*?)" class="video-title">', text_data)[0]
        mp4_url_data = re.findall(r"<script>window.__playinfo__=(.*?)</script>", text_data)[0]
        json_data = json.loads(mp4_url_data)
        audio_url = json_data["data"]["dash"]["audio"][0]["baseUrl"]
        video_url = json_data["data"]["dash"]["video"][0]["baseUrl"]
        print("数据提取完毕...")
        self.save_data(video_title, audio_url, video_url)

    def save_data(self, video_title, audio_url, video_url):
        try:
            os.mkdir('./data')
        finally:
            # 保存音频数据
            print("正在保存音频数据...")
            audio_data = requests.get(audio_url, headers=self.headers).content
            with open(f"./data/{video_title}.mp3", "wb") as w:
                w.write(audio_data)
                print("音频数据保存完毕...")

            # 保存视频数据
            print("正在保存视频数据...")
            video_data = requests.get(video_url, headers=self.headers).content
            with open(f"./data/{video_title}.mp4", "wb") as w:
                w.write(video_data)
                print("视频数据保存完毕...")

            # 合并音频和视频
            self.combined_data(video_title)

    def combined_data(self, video_title):
        # 需要将ffmpeg配置到环境变量
        final_data = f'ffmpeg -i data/{video_title}.mp4 -i data/{video_title}.mp3 -c:v copy -c:a aac -strict experimental data/_{video_title}.mp4'
        subprocess.run(final_data, shell=True)
        # os.system(final_data)
        self.move_other(video_title)

    def move_other(self, video_title):
        os.remove(f'./data/{video_title}.mp3')
        os.remove(f'./data/{video_title}.mp4')


if __name__ == '__main__':
    task = []
    name = input("请输入视频链接：")
    while name != 'q':
        task.append(name)
        name = input("继续输入视频链接(输入q结束)：")
    spider = DownloadVideo(task)
    spider.run()
