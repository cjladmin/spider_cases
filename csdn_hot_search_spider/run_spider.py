# encoding: utf-8
# @Time : 2022/4/16 19:30
# @Author : Torres-圣君
# @File : get_page_data.py
# @Sofaware : PyCharm
from .get_data import *
from .save_data import *
import time


# 获取所有文章分类
def get_type():
    all_type_url = 'https://img-home.csdnimg.cn/data_json/jsconfig/rank_nav_list.json'
    headers = {
        "user-agent": get_user_agent()
    }
    res = requests.get(all_type_url, headers=headers)
    type_json = res.json()
    return type_json["list"]


def run():
    # 调用get_type方法，获取所有文章分类
    all_type_list = get_type()
    # 实例化SavaData类
    b = SavaData()
    for i in range(0, len(all_type_list)):
        # 获取具体分类的名称
        type_ = all_type_list[i]["type"]
        print(f"开始获取<{type_}>的热榜文章！")
        # 创建文件并打开
        b.open(type_)
        for j in range(0, 8):
            # 实例化CsdnHot类
            d = CsdnHot(j, type_)
            # 调用get_data方法请求目标网址
            data = d.get_data()
            # 调用save_data方法保存返回的数据
            b.sava_data(j, data)
            # break
        # 关闭文件
        b.close()
        print(f"<{type_}>的热榜抓取完毕！")
        # 每切换一种分类就休息2秒，防止访问频率过快被封IP
        time.sleep(2)
        # break


if __name__ == '__main__':
    run()
