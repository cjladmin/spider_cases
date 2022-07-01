# encoding: utf-8
# @Time : 2022/5/10 19:18
# @Author : Torres-圣君
# @File : run_spider.py
# @Software : PyCharm
import os
import csv
from playwright.sync_api import sync_playwright


class LagouJbos:
    def __init__(self, job_name):
        self.job_name = job_name
        self.url = "https://www.lagou.com/jobs/list_" + job_name
        self.flag = True

    def get_page_data(self):
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page()
            page.goto(self.url)
            # 获取总页数
            page_max = page.locator('xpath=//*[@id="order"]/li/div[4]/div[3]/span[2]').text_content()
            print(f"共找到<{page_max}>页相关数据")
            self.is_file()
            for i in range(0, int(page_max)):
                print(f"正在获取第<{i+1}>页")
                self.get_jobs_data(page)
                print(f"第<{i+1}>页数据写入完毕，正在进入下一页...")
                page.click('xpath=//*[@id="order"]/li/div[4]/div[2]')
                page.screenshot(path=f"./data/lagou.png")
            browser.close()

    def get_jobs_data(self, page):
        try:
            jobs_data_list = page.query_selector_all('//*[@id="s_position_list"]/ul/li')
            # print(len(jobs_data_list))
            for jobs_data in jobs_data_list:
                item = dict()
                # 工作标题
                item['job_title'] = jobs_data.query_selector('xpath=./div[1]/div[1]/div[1]/a/h3').text_content()
                # 工作链接
                item['job_link'] = jobs_data.query_selector('xpath=./div[1]/div[1]/div[1]/a').get_attribute('href')
                # 公司名称
                item['job_company'] = jobs_data.query_selector('xpath=./div[1]/div[2]/div[1]/a').text_content().strip('\n')
                # 薪资范围
                item['job_price'] = jobs_data.query_selector('xpath=./div[1]/div[1]/div[2]/div/span').text_content()
                # 投递要求
                item['job_demand'] = jobs_data.query_selector('xpath=./div[1]/div[1]/div[2]/div').text_content().strip(' \n').split('\n')[-1]
                # 公司地址
                item['job_address'] = jobs_data.query_selector('xpath=./div[1]/div[1]/div[1]/a/span/em').text_content()
                # 将数据保存为csv格式
                self.save_data(item)
        except:
            pass

    def save_data(self, item):
        # 写入的数据为字典类型
        with open(f'./data/{self.job_name}.csv', 'a', newline='') as w:
            # 创建一个csv的DictWriter对象
            w_csv = csv.DictWriter(w, ['job_title', 'job_link', 'job_company', 'job_price', 'job_demand', 'job_address'])
            if self.flag:
                # 写入一行当表头，即字典键名
                w_csv.writeheader()
                self.flag = False
            # 写入对行数据，即字典的所有值
            w_csv.writerow(item)

    def is_file(self):
        try:
            # 检测文件是否存在，用于相同工作二次执行
            os.remove(f'./data/{self.job_name}.csv')
        except:
            pass


if __name__ == '__main__':
    job_name = input("请输入职位名称：")
    lagou = LagouJbos(job_name)
    lagou.get_page_data()
