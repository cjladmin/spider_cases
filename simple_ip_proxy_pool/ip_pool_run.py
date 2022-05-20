# encoding: utf-8
# @Time : 2022/4/23 10:05
# @Author : Torres-圣君
# @File : ip_poop_run.py
# @Sofaware : PyCharm
import asyncio
from all_ip_agent import get_66ip, get_89ip, get_ip3366, get_ihuan, get_kuaidaili, get_jiangxianli
import threading
import os


def thread_run(num):
    threads = [
        threading.Thread(target=get_66ip.get_data, args=(num,)),
        threading.Thread(target=get_89ip.get_data, args=(num,)),
        threading.Thread(target=get_ip3366.get_data, args=(num,)),
        threading.Thread(target=get_ihuan.get_data, args=(num,)),
        threading.Thread(target=get_kuaidaili.get_data, args=(num,)),
        threading.Thread(target=get_jiangxianli.get_data, args=(num,)),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    try:
        os.remove("ip_pool.json")
    except:
        pass
    finally:
        # 爬取所有网站前10页可用的IP代理
        thread_run(5)
        print("爬取完毕！")
