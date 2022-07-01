# encoding: utf-8
# @Time : 2022/6/30 14:55
# @Author : Torres-圣君
# @File : run_spider.py
# @Software : PyCharm
import requests
import re
import time
from lxml import etree
import pytesseract
from PIL import Image


class DetailedData:
    def __init__(self, page_num):
        self.urls = [f'https://www.ziroom.com/z/p{num + 1}/' for num in range(page_num)]
        self.headers = {
            "Cookie": "CURRENT_CITY_CODE=110000; CURRENT_CITY_NAME=%E5%8C%97%E4%BA%AC; _csrf=yjfN8G-kzNnGvj1iEvjH6O1x3TNy89d0; __jsluid_s=4174712fab682cd6df16575532ddfe6b; sajssdk_2015_cross_new_user=1; gr_user_id=383b4bb6-6a6b-4901-a057-9c620a3e2e26; __jsluid_h=1df213e6b4954e733185c9409be2a2e7; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22181b36097ea1b3-0f16d08755ce17-4f617f5b-1327104-181b36097eb316%22%2C%22%24device_id%22%3A%22181b36097ea1b3-0f16d08755ce17-4f617f5b-1327104-181b36097eb316%22%2C%22props%22%3A%7B%22%24latest_referrer%22%3A%22%22%2C%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37"
        }
        # 固定的数字位置
        self.position_list = ['-0px', '-21.4px', '-42.8px', '-64.2px', '-85.6px', '-107px', '-128.4px', '-149.8px', '-171.2px', '-192.6px']

    def run(self):
        for url in self.urls:
            self.page_data(url)
            time.sleep(5)

    def page_data(self, url):
        res = requests.get(url, headers=self.headers).text
        # 保存数字背景图片
        self.download_img(res)
        # 使用ocr识别图片
        fonts_dic = self.ocr_fonts()
        print(fonts_dic)
        html = etree.HTML(res)
        div_list = html.xpath('//div[@class="Z_list-box"]/div')
        for div in div_list:
            room_link = "https:" + div.xpath('./div[2]/h5/a/@href')[0]
            title = div.xpath('./div[2]/h5/a/text()')[0]
            area = div.xpath('./div[2]/div[1]/div[1]/text()')[0]
            address = div.xpath('./div[2]/div[1]/div[2]/text()')[0].strip()
            bg_link = div.xpath('.//span[@class="num"]/@style')
            price = self.decrypt_font(bg_link, fonts_dic)
            item = [room_link, title, area, address, price]
            print(item)
            self.save_data(item)

    def download_img(self, res):
        # 在页面源码中提取图片链接
        img = re.findall(r'//static8.ziroom.com/phoenix/pc/images/price/new-list/(.*?)\);', res)[0]
        img_url = "https://static8.ziroom.com/phoenix/pc/images/price/new-list/" + img
        # 以二进制写入文件保存图片
        img_data = requests.get(img_url, headers=self.headers).content
        with open('ocr_img/bg_image.png', 'wb') as w:
            w.write(img_data)

    def ocr_fonts(self):
        # 纯白背景图
        white_img = Image.open('ocr_img/black_img.png')
        # 数字背景图
        bg_img = Image.open('ocr_img/bg_image.png')
        # 改变图像尺寸
        img1 = white_img.resize((600, 100))
        img2 = bg_img.resize((560, 60))
        # 合并两个图像，bg_img 放到 white_img 并指定坐标(不能完全重叠)
        img1.paste(img2, (30, 20))
        # 保存图片
        img1.save("text.png")
        # 使用合并后的图
        image = Image.open('ocr_img/text.png')
        # 图片二值化，便于ocr识别
        Img = image.convert('L')
        # 识别提取图片中的内容
        text = pytesseract.image_to_string(Img)
        # 将内容写入列表
        nums = [num for num in text if num != " "]
        fonts_dic = {}
        # 把位置和数字存放为字典
        for k, v in zip(self.position_list, nums):
            fonts_dic[k] = v
        return fonts_dic

    def decrypt_font(self, bg_link, fonts_dic):
        price_list = []
        # 替换价格的每个数字
        for bg in bg_link:
            position = bg.split(" ")[-1]
            num = fonts_dic[position]
            price_list.append(num)
        # 拼接成完整的价格
        price = ''.join(price_list) + "元/月"
        return price

    def save_data(self, item):
        with open('自如网租房房源信息.csv', 'a+') as w:
            w.seek(0)
            flag = w.read() == ""
            if flag:
                w.write("链接,标题,面积,地址,房价\n")
            w.write(','.join(item) + "\n")


if __name__ == '__main__':
    page_num = int(input("请输入需要获取的页码："))
    dd = DetailedData(page_num)
    dd.run()
