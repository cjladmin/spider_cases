# encoding: utf-8
# @Time : 2022/7/2 22:51
# @Author : Torres-圣君
import requests
import execjs


def run(text):
    url = "https://fanyi.baidu.com/v2transapi?from=en&to=zh"
    headers = {
        "Cookie": "BIDUPSID=3A2B984F3D5B346B085AD5B5865CD243; PSTM=1620650820; __yjs_duid=1_90335d2ecbd02d6fabe6c844263de3b31620818982804; REALTIME_TRANS_SWITCH=1; HISTORY_SWITCH=1; FANYI_WORD_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; MCITY=-%3A; BAIDUID=9E5B8CC930FAAF06F999A3B216168E7A:FG=1; APPGUIDE_10_0_2=1; BDUSS=JSbjBTaDAzVkRNYzJnbVJPY35mZmZEQTNxN0JCb1lBSXNvd2lieVJ5ZnZkOUZpRVFBQUFBJCQAAAAAAAAAAAEAAADkEyraVG9ycmVzyqW-~QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAO~qqWLv6qliQW; BDUSS_BFESS=JSbjBTaDAzVkRNYzJnbVJPY35mZmZEQTNxN0JCb1lBSXNvd2lieVJ5ZnZkOUZpRVFBQUFBJCQAAAAAAAAAAAEAAADkEyraVG9ycmVzyqW-~QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAO~qqWLv6qliQW; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1655206845,1655616330; ZFY=XmZ2OfobadeEG7DawlXrwhekRikKh5VFZ62dA6HB2JY:C; BAIDUID_BFESS=C1F2EB92F00DFE8F8EC8F5B5023D2982:FG=1; BA_HECTOR=8k8h8l8l8la02025041hbvh2q14; ab_sr=1.0.1_Y2RmZWRhZDVjZGQ2NTc3MzY4ZWVkZmU1NzkzNjFkMWI2MjM4MjRhMDllMmY2MTVjOTcxYWZiYjY2NDFmNWNiYmYxZjEzN2JlN2EyZjRiYzNiMjY5NWZiYWI5ZTljNmYzNjlmMjgxMzEzMzJjNjViNDdmYzViNjA4YzFkZDZhMWYyZDEyYmI5MzYyOTc3MTU2NjNhODE2ZGRjMWI1MTRkZjlkNzI4OTFjY2U4OTBiYTRkYjUzN2Y5NjRkMjA1NmRl",
        "Referer": "https://fanyi.baidu.com/translate",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44"
    }
    res = requests.post(url, headers=headers, data=get_data(text))
    data = res.json()
    print(f"{'-'*100}\n", data['trans_result']['data'][0]['dst'])


def get_data(text):
    x1, x2 = is_chinese(text)
    data = {
        "from": x1,
        "to": x2,
        "query": text,
        "transtype": "realtime",
        "simple_means_flag": "3",
        "sign": decrypt_params(text),
        "token": "8f8d536955d93b439ca12bb1977f5195",
        "domain": "common",
    }
    # print(data)
    return data


def is_chinese(check_str):
    # 判断字符串中是否含有中文
    for ch in check_str:
        if u'⼀' <= ch <= u'󰀀':
            return "zh", "en"
        else:
            return "en", "zh"


def decrypt_params(text):
    with open("demo.js", 'r') as r:
        # 读取js文件，使用compile加载js代码并执行
        js = r.read()
        js_func = execjs.compile(js)
        js_data = js_func.call("e", text)
        # print(js_data)
    return js_data


if __name__ == '__main__':
    content = input("请输入需要翻译的内容：")
    run(content)
