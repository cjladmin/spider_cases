# encoding: utf-8
# @Time : 2022/6/25 15:36
# @Author : Torres-圣君
# @File : decrypt_fonts.py
# @Software : PyCharm
import json
from fontTools.ttLib import TTFont


def decrypt_font(page_res):
    # 读取解密字典
    with open('./woff/fonts_dic.json', 'r', encoding='utf-8') as r:
        fonts_dic = json.loads(r.read())
    # 替换网页源码中的所有加密文字，当然也可以在提取到数据后再解密
    for i in fonts_dic:
        if str(i) in page_res:
            page_res = page_res.replace(str(i), fonts_dic[i].replace(';', ''))
    # 返回解密后的网页源码
    return page_res


def save_fonts_dic():
    words = '1234567890店中美家馆小车大市公酒行国品发电金心业商司超生装园场食有新限天面工服海华水房饰城乐汽香部利子老艺花专东肉菜学福饭人百餐茶务通味所山区门药银农龙停尚安广鑫一容动南具源兴鲜记时机烤文康信果阳理锅宝达地儿衣特产西批坊州牛佳化五米修爱北养卖建材三会鸡室红站德王光名丽油院堂烧江社合星货型村自科快便日民营和活童明器烟育宾精屋经居庄石顺林尔县手厅销用好客火雅盛体旅之鞋辣作粉包楼校鱼平彩上吧保永万物教吃设医正造丰健点汤网庆技斯洗料配汇木缘加麻联卫川泰色世方寓风幼羊烫来高厂兰阿贝皮全女拉成云维贸道术运都口博河瑞宏京际路祥青镇厨培力惠连马鸿钢训影甲助窗布富牌头四多妆吉苑沙恒隆春干饼氏里二管诚制售嘉长轩杂副清计黄讯太鸭号街交与叉附近层旁对巷栋环省桥湖段乡厦府铺内侧元购前幢滨处向座下臬凤港开关景泉塘放昌线湾政步宁解白田町溪十八古双胜本单同九迎第台玉锦底后七斜期武岭松角纪朝峰六振珠局岗洲横边济井办汉代临弄团外塔杨铁浦字年岛陵原梅进荣友虹央桂沿事津凯莲丁秀柳集紫旗张谷的是不了很还个也这我就在以可到错没去过感次要比觉看得说常真们但最喜哈么别位能较境非为欢然他挺着价那意种想出员两推做排实分间甜度起满给热完格荐喝等其再几只现朋候样直而买于般豆量选奶打每评少算又因情找些份置适什蛋师气你姐棒试总定啊足级整带虾如态且尝主话强当更板知己无酸让入啦式笑赞片酱差像提队走嫩才刚午接重串回晚微周值费性桌拍跟块调糕'
    # 这里咱们想要获取的数据，在 num 和 address 中都有涉及
    font_num = TTFont('./woff/num.woff')
    font_address = TTFont('./woff/address.woff')
    # 提取字体库的编码
    font_num_list = font_num.getGlyphOrder()[2:]
    font_address_list = font_address.getGlyphOrder()[2:]
    # 用于存放加密字体的键值对
    fonts_dic = {}
    for i, v in enumerate(words):
        num_char = font_num_list[i].replace("uni", "&#x").lower() + ';'
        fonts_dic[num_char] = v
        address_char = font_address_list[i].replace("uni", "&#x").lower() + ';'
        if address_char in fonts_dic:
            continue
        fonts_dic[address_char] = v
    with open('./woff/fonts_dic.json', 'w', encoding='utf-8') as w:
        json_data = json.dumps(fonts_dic, indent=1, ensure_ascii=False)
        w.write(json_data)
