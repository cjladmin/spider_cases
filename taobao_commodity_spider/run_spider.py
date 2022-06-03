# encoding: utf-8
# @Time : 2022/4/24 14:57
# @Author : Torres-圣君
# @File : douban_run_spider.py
# @Sofaware : PyCharm
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains as ac
import random
import time
import re
import json


class SaveTaobaoData:
    def __init__(self, search_content):
        self.search_content = search_content
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.execute_cdp_cmd(
            'Page.addScriptToEvaluateOnNewDocument',
            {
                'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
            }
        )

    def get_page(self):
        # 访问淘宝网址
        self.driver.get('https://www.taobao.com/')
        time.sleep(3)  # 停一会防止出意外

        # 向搜索框中添加内容，并按下回车进行搜索
        self.driver.find_element_by_xpath("//input[@aria-label='请输入搜索文字']").send_keys(self.search_content, Keys.ENTER)

        # 扫码登陆
        self.driver.find_element_by_xpath('//*[@id="login"]/div[1]/i').click()
        # 给20秒时间登陆自己的账号，根据自己的速度来
        time.sleep(20)

        # 获取关键字商品的总页数
        get_page_number = self.driver.find_element_by_xpath('//*[@id="mainsrp-pager"]/div/div/div/div[1]').text
        page_number = int(re.findall(r'(\d+)', get_page_number)[0])
        print(page_number)

        # 解析页面提取数据
        self.get_page_data()
        # 进入下一页
        self.get_next_page(self.driver, page_number)

    def get_page_data(self):
        # 模拟真人操作，拖动滚动条
        for x in range(1, 11, 2):
            time.sleep(0.5)
            j = x / 10
            js = 'document.documentElement.scrollTop = document.documentElement.scrollHeight * %f' % j
            self.driver.execute_script(js)
        # 页面存放的所有商品
        div_list = self.driver.find_elements_by_xpath('//*[@id="mainsrp-itemlist"]/div/div/div[1]/div')
        print("当前页面的总商品数：", len(div_list))
        data_list = []
        for div in div_list:
            item = dict()
            # 商品标题
            item["title"] = div.find_element_by_xpath('./div[2]/div[2]/a').text.strip(" \t\n")
            # 商品价格
            item["price"] = div.find_element_by_xpath('./div[2]/div[1]/div[1]/strong').text + "元"
            # 商品销量
            item["number"] = div.find_element_by_xpath('./div[2]/div[1]/div[2]').text
            # 店铺名称
            item["shop"] = div.find_element_by_xpath('./div[2]/div[3]/div[1]/a/span[2]').text
            # 商品链接
            item["link"] = div.find_element_by_xpath('./div/div/div[1]/a').get_attribute('href').strip(" \t\n")
            # 展示爬取到的数据
            print(item)
            # 追加进列表
            data_list.append(item)
        # 保存数据
        self.save_data(data_list)

    def get_next_page(self, driver, page_number):
        for i in range(44, page_number*44, 44):
            # 构造每页的链接
            self.driver.get(f"https://s.taobao.com/search?q={self.search_content}&s={i}")
            # 隐式等待
            self.driver.implicitly_wait(10)
            # 判断是否出现验证码
            content = driver.page_source
            if "亲，请拖动下方滑块完成验证" in content:
                con = self.hua_kuai(driver)
                count = 0
                while "亲，请拖动下方滑块完成验证" in con and count <= 3:
                    con = self.hua_kuai(driver)
                    count += 1
                    if count == 3:
                        print("已尽力尝试自动滑动验证码，但抱歉没能通过，请手动滑一下吧~")
                        input("正在等待手动滑动，滑动完成后按回车！")
            # 解析页面数据
            self.get_page_data()

    def save_data(self, data_list):
        # 转为JSON格式
        data = json.dumps(data_list, indent=1, ensure_ascii=False)
        # 记录当前时间
        t = time.localtime()
        ft = time.strftime("%Y-%m-%d %H:%M", t)
        # 打开文件写入数据
        with open(f"data/{self.search_content}_商品信息.json", "a", encoding="utf-8") as w:
            w.write(f'"{ft}": ' + data + ",")

    def hua_kuai(self, driver):
        print("触发验证码系统，正在自动处理！")
        img = driver.find_element_by_xpath('//*[@id="nc_1__scale_text"]/span')
        size = img.size
        # 标签宽度
        rangle_x = size['width']
        ele = driver.find_element_by_xpath('//*[@id="nc_1_n1z"]')
        print("验证码框体宽度：", rangle_x)
        button_location = ele.location
        # 滑块的y轴位置
        rangle_y = button_location['y']
        print("滑块的y轴位置：：", rangle_y)
        # 按住滑块元素不放
        ac(driver).click_and_hold(ele).perform()
        # 拖动滑块
        ac(driver).move_by_offset(300, random.randint(-5, 5)).perform()
        # 松开鼠标
        ac(driver).release().perform()
        # 加载页面
        time.sleep(2)
        try:
            # 点击重新滑动按钮
            driver.find_element_by_xpath('//*[@id="`nc_1_refresh1`"]').click()
        except:
            pass
        return driver.page_source


if __name__ == '__main__':
    text = input("请输入需要搜索的关键字：")
    run_spider = SaveTaobaoData(text)
    run_spider.get_page()
