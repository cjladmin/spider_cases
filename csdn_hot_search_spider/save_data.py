# encoding: utf-8
# @Time : 2022/4/16 19:49
# @Author : Torres-圣君
# @File : save_data.py
# @Sofaware : PyCharm
import json
import time


class SavaData:
    def open(self, type_):
        self.w = open(rf"data/{type_.replace('/','_')}.json", "w", encoding="utf-8")

    def sava_data(self, page, data):
        # 获取当前日期
        t = time.localtime()
        now = time.strftime("%Y-%m-%d %H:%M", t)
        # 将日期和数据合成字典
        item = {
            f"<第{page+1}页> | {now}": data
        }
        # 将字典转为JSON格式
        data = json.dumps(item, indent=1, ensure_ascii=False)
        # 写入数据
        self.w.write(data)

    def close(self):
        self.w.close()
