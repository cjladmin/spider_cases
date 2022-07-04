# encoding: utf-8
# @Time : 2022/5/3 23:23
# @Author : Torres-圣君
# @File : run_spider.py
# @Software : PyCharm
import json
import requests

url = "https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=diseaseh5Shelf"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44"
}


def run(city):
    res = requests.get(url, headers=headers).json()
    all_data = res['data']['diseaseh5Shelf']
    last_update_time = all_data["lastUpdateTime"]
    # 保存城市列表
    save_city_list(all_data)
    # 读取城市名称列表
    city_list = json.loads(open("city_list.json", encoding='utf-8').read())
    city = city.strip("省市")
    if city == "中国":
        data_ = all_data["areaTree"][0]
    else:
        try:
            if city in city_list["省"]:
                # 提取当前省份的所有数据
                data_ = [x for x in all_data["areaTree"][0]["children"] if x["name"] == city][0]
            elif city in city_list["市"]:
                # 提取当前城市的所有数据
                data_ = [y for x in all_data["areaTree"][0]["children"] for y in x["children"] if y["name"] == city][0]
            else:
                return f"没有查询到{city}的疫情数据~"
        except IndexError:
            return "疫情接口出现异常，请稍后重试~"
    confirm = data_["total"]["confirm"]          # 累计确诊
    heal = data_["total"]["heal"]                # 累计治愈
    dead = data_["total"]["dead"]                # 累计死亡
    now_confirm = data_["total"]["nowConfirm"]   # 目前确诊
    add_confirm = data_["today"]["confirm"]      # 新增确诊
    return f"{city}疫情更新日期：\n" \
           f"{last_update_time}\n" \
           f"————————————————————————\n" \
           f"该地区疫情数据如下：\n" \
           f"新增确诊：{add_confirm}\n" \
           f"目前确诊：{now_confirm}\n" \
           f"累计确诊：{confirm}\n" \
           f"累计治愈：{heal}\n" \
           f"累计死亡：{dead}"


def save_city_list(all_data):
    with open("city_list.json", 'w', encoding='utf-8') as w:
        # 保存所有省份和城市名称
        sheng_list = []
        shi_list = []
        for i in all_data["areaTree"][0]["children"]:
            sheng_list.append(i["name"])
            sheng_list.append(i["name"]+"省")
            for j in i["children"]:
                shi_list.append(j["name"])
                shi_list.append(j["name"]+"市")
        dict_city = {
            "省": sheng_list,
            "市": shi_list
        }
        w.write(json.dumps(dict_city, indent=1, ensure_ascii=False))
        print("城市列表保存完成！")


city_name = input("请输入要查的城市名：")
print(run(city_name))
