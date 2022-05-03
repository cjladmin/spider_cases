# encoding: utf-8
# @Time : 2022/4/23 10:12
# @Author : Torres-圣君
# @File : get_ip3366.py
# @Sofaware : PyCharm
# https://proxy.ip3366.net/free/?action=china&page=1
import asyncio
import aiohttp
from user_agent import get_ua
from test_save import test_ip
from lxml import etree


def get_data(num):
    loop_ = asyncio.new_event_loop()
    asyncio.set_event_loop(loop_)
    loop = asyncio.get_event_loop()
    urls = [f"https://proxy.ip3366.net/free/?action=china&page={str(i)}" for i in range(1, num+1)]
    tasks = [loop.create_task(parse(url)) for url in urls]
    loop.run_until_complete(asyncio.wait(tasks))


async def parse(url):
    try:
        headers = {
            "User-Agent": get_ua()
        }
        timeout = aiohttp.ClientTimeout(total=1000)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, headers=headers) as res:
                page = etree.HTML(await res.text())
                ip_list = page.xpath('//*[@id="content"]/section/div[2]/table//tr')
                del ip_list[0]
                # print(len(ip_list))
                for i in range(1, len(ip_list)):
                    # 提取ip地址
                    ip_address = ip_list[i].xpath(f'./td[1]/text()')[0]
                    # 提取ip端口
                    ip_port = ip_list[i].xpath(f'./td[2]/text()')[0]
                    # 提取ip类型
                    ip_type = ip_list[i].xpath(f'./td[4]/text()')[0]
                    if ip_type == "HTTPS":
                        # 去除无用字符，并拼接为ip可用格式
                        ip_msg = "https://" + ip_address.strip(" \t\n") + ":" + ip_port.strip(" \t\n")
                        poxyz = {
                            "https": ip_msg
                        }
                    else:
                        # 去除无用字符，并拼接为ip可用格式
                        ip_msg = "http://" + ip_address.strip(" \t\n") + ":" + ip_port.strip(" \t\n")
                        poxyz = {
                            "http": ip_msg
                        }
                    test_ip(poxyz)
    except IndexError:
        pass
