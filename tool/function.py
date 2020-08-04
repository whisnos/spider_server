import hashlib
import pymssql
import random
import uuid


def MD5encrypt(text):
    ''' md5加密 '''
    m5 = hashlib.md5(text.encode('utf-8'))
    return m5.hexdigest()


def get_uuid():
    # 获取一个随机字符串
    return str(uuid.uuid4())


def verify_num(value):
    # 判断是否是纯数字
    try:
        if isinstance(value, str):
            return int(value)
        else:
            return False
    except ValueError as e:
        return False


def Return_headers():
    USER_AGENT = [
        "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36 115Browser/8.6.0",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; Trident/7.0; ASJB; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.5155.400 QQBrowser/9.7.13231.400",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3298.4 Safari/537.36",
    ]
    user_ag = random.choice(USER_AGENT)
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "max-age=0",
        # "cookie": "cna=xRiMF2LAS3oCAXnPggl02zvR; lid=%E7%BA%AF%E9%87%91%E7%8C%AA%E7%8C%AA; enc=0JJWfHkdbx6vwJaUYwMijNcVxu0G1bmNMlF8cnCsqcFs9mXmQRG%2F6h%2F%2FRzp0H8JjA0i9imfIMrajHWDapU8sCA%3D%3D; t=0fb2a36c00cbe9f34230f6daa30c9b02; tracknick=%5Cu7EAF%5Cu91D1%5Cu732A%5Cu732A; lgc=%5Cu7EAF%5Cu91D1%5Cu732A%5Cu732A; _tb_token_=ee3b535febe73; cookie2=11683b92a6174ab44ca3eeb946cf7bf4; dnk=%5Cu7EAF%5Cu91D1%5Cu732A%5Cu732A; uc1=cookie21=V32FPkk%2FhodqgY9Lqf5dEg%3D%3D&cookie16=V32FPkk%2FxXMk5UvIbNtImtMfJQ%3D%3D&pas=0&cookie15=URm48syIIVrSKA%3D%3D&cookie14=UoTV6OOAKbMoEQ%3D%3D&existShop=true; uc3=nk2=13MctR4KUoQ%3D&vt3=F8dBxGJkmmQGAE06jNk%3D&id2=UNJXwAw5pyqt&lg2=UtASsssmOIJ0bQ%3D%3D; uc4=nk4=0%401bwfHinaO3lGfbNRFOr02ZQ5iA%3D%3D&id4=0%40UgXQysjHsRIXCi48wgKxoKLkx1c%3D; _l_g_=Ug%3D%3D; unb=326621184; cookie1=WvFfxcUdGYC1tTPQndOB0qqxoocWWDnX1hz%2BEwLk4p0%3D; login=true; cookie17=UNJXwAw5pyqt; _nk_=%5Cu7EAF%5Cu91D1%5Cu732A%5Cu732A; sgcookie=EJe%2BavB6sjzjnbxpn0nLg; sg=%E7%8C%AA41; csg=64f32048; _m_h5_tk=256a171115d315ad0e72c176d766ec8f_1594291367309; _m_h5_tk_enc=916c9eb6a38d9f06204a2cdff82d2070; x5sec=7b22726174656d616e616765723b32223a226438393334323932633139393462646134373462323763313238376663383934434b4f326d2f6746454c44743662546d6c4c4b3832674561437a4d794e6a59794d5445344e447378227d; l=eB_orpDeOObUDNKNKOfZnurza77T_IRfguPzaNbMiOCPOp5M5EEVWZlyQ9THCnGVnsiyR3ow4YKgBuL76y4EhZXRFJXn9MptndLh.; isg=BGFhVPCumjazIjZBufSSEp98cC17DtUAqE563MM2R2jGKoD8C1r-0aEsjF6s4m04",
        # "cookie": "t=e3ced4867bbbb33ad8e43a6664f1b440; thw=cn; cookie2=1ae89e1b7eb4f38050c2a8484ca7f9e3; _tb_token_=fe3fdd7e7787e; enc=FCtEbwsd4d4qFaGEEU1%2Bh6zQqkT31zH7ZjTng%2ByjgFV1IKn98igFAnRQ80yP1MGcCWXDBuTJBB%2Fv2BN0HrnsFw%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; cna=cfrcFZLIz0UCAXxBtKpIjGyJ; v=0; unb=3342625761; uc3=vt3=F8dByucj%2BPu98CEsPjg%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D&id2=UNN5E%2BCNxCTmeQ%3D%3D&nk2=symzrp14SFvM8w%3D%3D; csg=e158c6a6; lgc=%5Cu5C0F%5Cu9F99cxcgao; cookie17=UNN5E%2BCNxCTmeQ%3D%3D; dnk=%5Cu5C0F%5Cu9F99cxcgao; skt=5acee91bdd655b99; existShop=MTU3MTk4NzgwNA%3D%3D; uc4=id4=0%40UgQxlJz5L5Tdls4BK%2BsdqbH4MLk8&nk4=0%40sVYTNakktI2J71HcZK%2B0xxDC%2BDng; tracknick=%5Cu5C0F%5Cu9F99cxcgao; _cc_=W5iHLLyFfA%3D%3D; tg=0; _l_g_=Ug%3D%3D; sg=o1f; _nk_=%5Cu5C0F%5Cu9F99cxcgao; cookie1=B0OsmmuZ3XRBlfT4RmnPR0sbhg2pIYLBZ6M6p3hMTnE%3D; uc1=cookie16=U%2BGCWk%2F74Mx5tgzv3dWpnhjPaQ%3D%3D&cookie21=UtASsssmeW6lpyd%2BB%2B3t&cookie15=Vq8l%2BKCLz3%2F65A%3D%3D&existShop=false&pas=0&cookie14=UoTbnKo8UDBHXA%3D%3D&tag=8&lng=zh_CN; mt=ci=0_1; l=dBgSXBauqGXlvNsDBOCwVuI8YdQOAIRAguPRwhApi_5B9_T6fvbOkZkD2E96cjWftzTB4DlUQKv9-etXiDt6Qtk8sxAJvxDc.; isg=BNLSgblL29-ZPicjbaEizx2QI550S9VMW8fzYZwrzgVwr3KphHIYjcTNG0s2304V",
        "cookie": "t=8a9c256c3ea997fb8e10e6b3bd56d870; _tb_token_=356b8035ab8b6; cookie2=1dc9d680ee58ef6de89cd49f3ff815b7; cna=Hk8hF6TBIwwCASQaLEIBciME; isg=BLm5X-6BwqvMYJ4_jSaM2VxoyyWTxq14jAVT79vujuBTYtj0IxdySAY04OaUQUWw; l=eB_yNmrnOODQFB56KO5BFurza77TwIR48kPzaNbMiInca661_eEI7NQqiCCk8dtfgtCEfetz4d6Wyd3v8Q4LgZqhuJ1REpZZnxvO.; dnk=%5Cu5FC3%5Cu96E8081109; uc1=existShop=false&cookie21=URm48syIYB3rzvI4Dim4&cookie15=UtASsssmOIJ0bQ%3D%3D&cookie14=UoTV6OG7U0cRBQ%3D%3D&pas=0&cookie16=VT5L2FSpNgq6fDudInPRgavC%2BQ%3D%3D; uc3=lg2=Vq8l%2BKCLz3%2F65A%3D%3D&id2=UoYZYvhdDLQ4aw%3D%3D&nk2=s0y5hG2RUeKHZg%3D%3D&vt3=F8dBxGJqUG%2Fzq6m%2FwtU%3D; tracknick=%5Cu5FC3%5Cu96E8081109; lid=%E5%BF%83%E9%9B%A8081109; uc4=nk4=0%40sTNh9ZN2J%2FQTr0xQEkjJ%2B4c9bAq2&id4=0%40UO6QqfQDeUVyvy%2BNQTg6X%2F%2BVNLB3; _l_g_=Ug%3D%3D; unb=1778258141; lgc=%5Cu5FC3%5Cu96E8081109; cookie1=AQYNajBG8jxixbdnax0v0bizLWWCskSr1L5bq8XtDK4%3D; login=true; cookie17=UoYZYvhdDLQ4aw%3D%3D; _nk_=%5Cu5FC3%5Cu96E8081109; sgcookie=EAnhJMY%2BrkUkL58RBkPGv; sg=91a; csg=1aa635d9; enc=3cFqtLYMkxJg9OFLxFQv4ETJPLEPGY3pYnn%2Frlop9w96tL%2F6UTz3mz5vDTzzXvPTQ49qypw2hQ8vKEOzKq23eQ%3D%3D; x5sec=7b22726174656d616e616765723b32223a223062633730643835313534626338363636393733373239393834653562383533434d32516a2f6746454d33786a75756f334b653431674561444445334e7a67794e5467784e4445374d513d3d227d",
        "referer": "https://detail.tmall.com/item.htm?spm=a1z10.1-b-s.w4004-20100198398.2.12ca216fUtyKuv&id=556122214803&sku_properties=20509:28383",
        "user-agent": user_ag,
        "sec-fetch-dest": "script",
        "sec-fetch-mode": "no-cors",
        "sec-fetch-site": "same-site", }
    return headers


def return_sqlserver_connect():
    # 172.17.146.39 192.168.32.24
    try:
        conn = pymssql.connect(host='172.17.146.39', port='1433', user='sa', password='shanpengfei@no1',
                               database='TaoKe')
        cur = conn.cursor(as_dict=True)
    except Exception as e:
        return False, False
    return cur, conn


if __name__ == '__main__':
    import time

    stamp = int(time.time())
    sign = MD5encrypt('pLEcUd0v8BXaEnOF' + str(stamp))
    print(stamp)
    print(sign)
