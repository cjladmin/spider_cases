# encoding: utf-8
# @Time : 2022/6/29 10:20
# @Author : Torres-圣君
# @File : run_spider.py
# @Software : PyCharm
import requests

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37"
}


def run(author_id):
    count = 0
    while True:
        count += 1
        url = f"https://www.ximalaya.com/revision/album/v1/getTracksList?albumId={author_id}&pageNum={count}&sort=0"
        res = requests.get(url, headers=headers)
        audio_link_lisk = res.json()['data']['tracks']
        if len(audio_link_lisk) == 0:
            print("所有音频爬取完毕！")
            break
        else:
            for audio_link in audio_link_lisk:
                audio_title = audio_link['title']
                audio_id = audio_link['trackId']
                audio_url = f"https://www.ximalaya.com/revision/play/v1/audio?id={audio_id}&ptype=1"
                print("正在保存：", audio_title)
                save_audio(audio_title, audio_url)


def save_audio(audio_title, audio_url):
    audio_res = requests.get(audio_url, headers=headers).json()['data']['src']
    audio_data = requests.get(audio_res, headers=headers).content
    with open(f'{audio_title}.mp3', 'wb') as w:
        w.write(audio_data)
        print(audio_title, "保存完成！")


if __name__ == '__main__':
    # 作者ID
    author_id = 10092072
    run(author_id)
