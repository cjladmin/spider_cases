# encoding: utf-8
# @Time : 2022/6/23 15:19
# @Author : Torres-圣君
# @File : get_message.py
# @Software : PyCharm
import requests


class OtherData:
    def __init__(self, headers):
        self.url = "https://push2.eastmoney.com/api/qt/ulist.np/get"
        self.headers = headers

    def join_type1_params(self, page_data):
        secids_list = []
        for i in page_data:
            # HK_开头的为港股市场，代码前加116.
            if i[2].startswith('HK_'):
                i[2] = i[2].replace("HK_", "")
                secids_list.append(f'116.{i[2]}')
            # NASDAQ_开头的为美股市场，代码前加105.
            elif i[2].startswith('NASDAQ_'):
                i[2] = i[2].replace("NASDAQ_", "")
                secids_list.append(f'105.{i[2]}')
            # NYSE_开头的为美股市场，代码前加106.
            elif i[2].startswith('NYSE_'):
                i[2] = i[2].replace("NYSE_", "")
                secids_list.append(f'106.{i[2]}')
            # AMEX_开头的为美股市场，代码前加107.
            elif i[2].startswith('AMEX_'):
                i[2] = i[2].replace("AMEX_", "")
                secids_list.append(f'107.{i[2]}')
            # 数字6开头的为A股市场，代码前加1.
            elif i[2].startswith('6'):
                secids_list.append(f'1.{i[2]}')
            else:
                secids_list.append(f'0.{i[2]}')
        params = {
            "fltt": 2,
            "np": 3,
            "ut": "a79f54e3d4c8d44e494efb8f748db291",
            "invt": 2,
            "secids": ",".join(secids_list),
            "fields": "f1,f2,f3,f4,f12,f13,f14,f152,f15,f16",
        }
        print(params)
        return params

    def get_response(self, page_data):
        params = self.join_type1_params(page_data)
        res = requests.get(self.url, headers=self.headers, params=params).json()
        page_other_data = []
        for data in res['data']['diff']:
            item = [
                data['f14'],
                data['f2'],
                data['f4'],
                str(data['f3'])+'%',
                data['f15'],
                data['f16']
            ]
            page_other_data.append(item)
            print(item)
        # 拼接完整的股票数据并返回
        page_all_data = [page_data[i]+page_other_data[i] for i in range(len(page_data))]
        return page_all_data
