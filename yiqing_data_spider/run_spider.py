# encoding: utf-8
# @Time : 2022/5/3 23:23
# @Author : Torres-圣君
# @File : douban_run_spider.py
# @Sofaware : PyCharm
import re
import requests

url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"


def run(city):
    res = requests.get(url)
    data = res.text
    yiqing_data = data.replace('"', "").replace('\\', "")
    result = re.findall(u'[\u4e00-\u9fa5]+', yiqing_data)
    if city in result:
        # 最近更新日期 lastUpdateTime
        lastUpdateTime = f'<{re.findall(r"lastUpdateTime:(.*),chinaTotal", yiqing_data)[0]}>'

        # 新增确诊人数 today_confirm
        today_confirm = "新增确诊：" + re.findall(f"{city}" + r".*?,today:{confirm:(\d+),", yiqing_data)[0] + "人"

        # 目前确诊人数 total_nowConfirm
        total_nowConfirm = "目前确诊：" + re.findall(f'{city}' + r".*?nowConfirm:(\d+),", yiqing_data)[0] + "人"

        # 累计确诊人数 total_confirm
        total_confirm = f"累计确诊：" + re.findall(rf"{city}.*?total:.*?confirm:(\d+),", yiqing_data)[0] + "人"

        # 累计治愈人数 total_heal
        total_heal = "累计治愈：" + re.findall(f'{city}' + r".*?heal:(\d+),", yiqing_data)[0] + "人"

        # 累计死亡人数 total_dead
        total_dead = "累计死亡：" + re.findall(f'{city}' + r".*?dead:(\d+),", yiqing_data)[0] + "人"

        return f"{city}疫情更新日期：\n" \
               f"{lastUpdateTime}\n" \
               f"————————————————————————\n" \
               f"该地区疫情数据如下：\n" \
               f"{today_confirm}\n" \
               f"{total_nowConfirm}\n" \
               f"{total_confirm}\n" \
               f"{total_heal}\n" \
               f"{total_dead}"
    else:
        return f"没有查询到{city}的疫情数据~"


city_name = input("请输入要查的城市名：")
print(run(city_name))
