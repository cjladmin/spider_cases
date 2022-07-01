# encoding: utf-8
# @Time : 2022/6/14 21:00
# @Author : Torres-圣君
# @File : run_spider.py
# @Software : PyCharm
import requests
import hashlib
import time


class YouDao(object):
    def __init__(self, word):
        self.word = word
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                          '99.0.4844.51 Safari/537.36 Edg/99.0.1150.39',
            'Cookie': 'OUTFOX_SEARCH_USER_ID=1277855906@10.108.160.101; OUTFOX_SEARCH_USER_ID_NCOO=1759159210.6581216; ___rl__test__cookies=1656644180767; fanyi-ad-id=307488; fanyi-ad-closed=0',
            'Referer': 'https://fanyi.youdao.com/'
        }

    def run(self):
        url = 'https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        res = requests.post(url, headers=self.headers, data=self.get_fromdata())
        data = res.json()
        print(f"{'-'*100}\n", data['translateResult'][0][0]['tgt'])

    def get_fromdata(self):
        """
            ts: "" + (new Date).getTime(),
            salt: ts + parseInt(10 * Math.random(), 10);,
            sign: n.md5("fanyideskweb" + e + i + "Ygy_4c=r#e#4EX^NUGUc5")
        """
        salt = str(int(time.time()*10000))  # 14位
        lts = str(int(time.time() * 1000))  # 13位

        # MD5加密
        data = "fanyideskweb" + self.word + salt + "Ygy_4c=r#e#4EX^NUGUc5"
        md5 = hashlib.md5()
        md5.update(data.encode())
        sign = md5.hexdigest()

        fromdata = {
            "i": self.word,
            "from": "AUTO",
            "to": "AUTO",
            "smartresult": "dict",
            "client": "fanyideskweb",
            "salt": salt,
            "sign": sign,
            "lts": lts,
            "bv": "8c5b4ecb9f7fdfe6b2997ab984775a98",
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_REALTlME"
        }
        return fromdata


if __name__ == '__main__':
    content = input("请输入需要翻译的内容：")
    youdao = YouDao(content)
    youdao.run()
