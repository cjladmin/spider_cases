# encoding: utf-8
# @Time : 2022/4/23 16:33
# @Author : Torres-圣君
# @File : get_jiangxianli.py
# @Sofaware : PyCharm
# https://ip.jiangxianli.com/blog.html?page=1
import asyncio
import aiohttp
from user_agent import get_ua
from test_save import test_ip
from lxml import etree


headers = {
    "User-Agent": get_ua()
}


def get_data(num):
    loop_ = asyncio.new_event_loop()
    asyncio.set_event_loop(loop_)
    loop = asyncio.get_event_loop()
    urls = [f"https://ip.jiangxianli.com/blog.html?page={str(int(i/5)+1)}" for i in range(1, num+1)]
    tasks = [loop.create_task(parse(url)) for url in urls]
    loop.run_until_complete(asyncio.wait(tasks))


async def get_page(url):
    try:
        timeout = aiohttp.ClientTimeout(total=1000)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, headers=headers, timeout=2) as res:
                page = etree.HTML(await res.text())
                div_list = page.xpath('//div[@class="contar-wrap"]/div')
                for div in div_list:
                    son_url = div.xpath('./div/h3/a/@href')[0]
                    await parse(son_url)
    except IndexError:
        pass


async def parse(son_url):
    try:
        timeout = aiohttp.ClientTimeout(total=1000)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(son_url, headers=headers) as res:
                page = etree.HTML(await res.text())
                ip_list = page.xpath('//div[@class="item"]/div/p/text()')
                for i in range(0, len(ip_list)):
                    # 去除无用字符，并拼接为ip可用格式
                    ip_msg = "http://" + ip_list[i].split("@")[0].strip(" \t\n")
                    poxyz = {
                        "http": ip_msg
                    }
                    test_ip(poxyz)
    except IndexError:
        pass
