# encoding: utf-8
# @Time : 2021/12/5 15:37
# @Author : Torres-圣君
# @File : get_page_data.py
# @Sofaware : PyCharm
import requests
import aiohttp
import asyncio
from lxml import etree


class uMeitu:
    def __init__(self):
        self.url = "https://www.umeitu.com/e/action/get_img_a.php"
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44',
        }

    def get_img_data(self, i: int):
        data = {
            "next": i,
            "table": "news",
            "action": "getmorenews",
            "limit": 10,
            "small_length": 120,
            "classid": 48
        }
        res = requests.post(self.url, headers=self.headers, data=data)
        page_data = etree.HTML(res.text)
        imgs_list = page_data.xpath('//ul/li/a')
        # 存放图片名称的列表
        task_name = []
        # 存放图片链接的列表
        task_link = []
        for img in imgs_list:
            # 图片名称
            img_name = img.xpath('./span/text()')[0]
            # 图片链接
            img_link = img.xpath('./img/@src')[0].replace("small", "")
            task_name.append(img_name)
            task_link.append(img_link)
        self.async_spider(task_name, task_link)

    async def download_imgs(self, img_name, img_link):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(img_link, headers=self.headers) as res:
                    with open(f'all_images/{img_name}.jpg', "wb") as w:
                        w.write(await res.content.read())
                        print(f"<{img_name}>下载完成")
        except Exception:
            pass

    def async_spider(self, task_name, task_link):
        # 获取事件循环
        loop = asyncio.get_event_loop()
        # 创建task列表
        tasks = [
            loop.create_task(self.download_imgs(task_name[i], task_link[i])) for i in range(0, len(task_name))
        ]
        # 执行爬虫事件列表
        loop.run_until_complete(asyncio.wait(tasks))

    def run(self):
        num = int(input("请输入要下载的图片页数："))
        for i in range(1, num+1):
            self.get_img_data(i)


if __name__ == '__main__':
    u = uMeitu()
    u.run()
