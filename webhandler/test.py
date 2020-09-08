import asyncio
import json

import tornado.web
from aiohttp_requests import requests

from tool.asynchttp import async_http_response
from tool.dbpool import DbOperate
from tool.async_redis_pool import RedisOperate
from sms.aliyunsms import send_aliyun_send_sms
from webhandler.basehandler import BaseHandler, check_login
from tool import applog, function
from config import TOKEN_TIME, SMS_VERIFY_TIME, SMS_TEMPLATE_DICT, DATABASE
import time


# import motor.motor_tornado
# client = motor.motor_tornado.MotorClient("127.0.0.1", 27017)
# db = client['spider']


# from motor.motor_asyncio import AsyncIOMotorClient
# connection = AsyncIOMotorClient("127.0.0.1", 27017)
# db = connection['spider']


async def run():
    async for doc in db.search_words_dtk.find({'id': 1}):
        print('doc', doc)
        return doc
        # db.search_words_dtk.update_one({'_id': doc.get('_id')}, {'$set': {'is_end': 0}})


class TestHandler(BaseHandler):

    async def get(self, *args, **kwargs):
        result = []
        print(2)
        # try:
        #     async with await DATABASE.transaction() as transaction:
        #         # 处理商品库存
        #         print(1)
        headers = {
            "Host":"api3-core-c-lq.amemv.com",
            "Connection":"keep-alive",
            "x-Tt-Token":"00394cd35500eb8ab3aa53594effe24e07fa9dc22850258a1de00148dbedb02ca92b87ca3d124996e930122749d9d96ee646",
            "sdk-version":"1",
            "User-Agent":"Aweme 11.1.0 rv:111015 (iPhone; iOS 12.1; zh_CN) Cronet",
            "X-SS-DP":"1128",
            "x-tt-trace-id":"00-1056994a099067e088f52ac977e50468-1056994a099067e0-01",
            "Accept-Encoding":"gzip, deflate, br",
            "Cookie":"d_ticket=332d257b0d9915e3baab26354d4904850558b; odin_tt=e72de93f38c19bc4b446b684d5084307be39f2623bdf2896a7a72c2b82a111d13da68ff99d7e1c2f69f329ea550bf1f1; sessionid=394cd35500eb8ab3aa53594effe24e07; sessionid_ss=394cd35500eb8ab3aa53594effe24e07; sid_guard=394cd35500eb8ab3aa53594effe24e07%7C1596028476%7C5184000%7CSun%2C+27-Sep-2020+13%3A14%3A36+GMT; sid_tt=394cd35500eb8ab3aa53594effe24e07; uid_tt=3c0ac05f4f520d1ae76d79f89e784e0f; uid_tt_ss=3c0ac05f4f520d1ae76d79f89e784e0f; install_id=3315770385767840; ttreq=1$1d6cca335eb21220eb05e1f9c9f288f3ee1124a1",
            "X-Khronos":"1598001943",
            "X-Gorgon":"8402c00c000015cd7f4a7f360a44985f1e2e22e39a9a6646f386",
            "x-common-params-v2":"channel=App%20Store&version_code=11.1.0&app_name=aweme&vid=7DE25B7C-8C79-4E51-8B6F-98E59AA3EDDD&app_version=11.1.0&mcc_mnc=46001&device_id=38763628687&aid=1128&screen_width=750&openudid=fb19224c28e96489a071098c581fcb6f167ed2e3&os_api=18&os_version=12.1&device_platform=iphone&build_number=111015&device_type=iPhone8,1&iid=3315770385767840&idfa=C6B24C79-AB73-4799-AE9B-3831440859FA&js_sdk_version=1.63.0.6&cdid=AC1136FE-C3EA-4029-974D-A4B0CEDEC43A",

        }
        url = 'https://api3-core-c-lq.amemv.com/aweme/v1/aweme/post/?ac=WIFI&is_vcd=1&publish_video_strategy_type=2&min_cursor=0&source=0&sec_user_id=MS4wLjABAAAAzcu8wS4HSxpwfzn720ajP2GQD6zn3j-90V9jY1-5QIs&count=21&user_id=97892293947&max_cursor=0&'

        # # 潘阳
        # url = 'https://api3-core-c-lq.amemv.com/aweme/v1/aweme/post/?ac=WIFI&is_vcd=1&publish_video_strategy_type=2&source=0&user_id=93166384405&count=12&sec_user_id=MS4wLjABAAAAfijqk17HwmIg_Q6Ag23xIolMOlOnK4xrvrJX2Th_RFM&max_cursor=1592385478000&'
        #
        # headers = {
        #     'Host': 'api5-core-c-lq.amemv.com',
        #     'Connection': 'keep-alive',
        #     'x-Tt-Token': '00394cd35500eb8ab3aa53594effe24e077f3b0b631fe4e45337ebe8ce3a7215a718db7b27927f3fc4c3b8263bba36a6c716',
        #     'sdk-version': '1',
        #     'User-Agent': 'Aweme 11.1.0 rv:111015 (iPhone; iOS 12.1; zh_CN) Cronet',
        #     'X-SS-DP': '1128',
        #     'x-tt-trace-id': '00-2ea6ef62099067e088f6f119b4540468-2ea6ef62099067e0-01',
        #     'Accept-Encoding': 'gzip, deflate, br',
        #     'Cookie': 'd_ticket=332d257b0d9915e3baab26354d4904850558b; odin_tt=e72de93f38c19bc4b446b684d5084307be39f2623bdf2896a7a72c2b82a111d13da68ff99d7e1c2f69f329ea550bf1f1; sessionid=394cd35500eb8ab3aa53594effe24e07; sessionid_ss=394cd35500eb8ab3aa53594effe24e07; sid_guard=394cd35500eb8ab3aa53594effe24e07%7C1598260898%7C5184000%7CFri%2C+23-Oct-2020+09%3A21%3A38+GMT; sid_tt=394cd35500eb8ab3aa53594effe24e07; uid_tt=3c0ac05f4f520d1ae76d79f89e784e0f; uid_tt_ss=3c0ac05f4f520d1ae76d79f89e784e0f; install_id=3315770385767840; ttreq=1$1d6cca335eb21220eb05e1f9c9f288f3ee1124a1',
        #     'X-Khronos': '1598510525',
        #     'X-Gorgon': '840240a300008195e8b36f31a283d52f661feed66796ee603e4a',
        #     'x-common-params-v2': 'channel=App%20Store&version_code=11.1.0&app_name=aweme&vid=7DE25B7C-8C79-4E51-8B6F-98E59AA3EDDD&app_version=11.1.0&mcc_mnc=46001&device_id=38763628687&aid=1128&screen_width=750&openudid=fb19224c28e96489a071098c581fcb6f167ed2e3&os_api=18&os_version=12.1&device_platform=iphone&build_number=111015&device_type=iPhone8,1&iid=3315770385767840&idfa=C6B24C79-AB73-4799-AE9B-3831440859FA&js_sdk_version=1.63.0.6&cdid=AC1136FE-C3EA-4029-974D-A4B0CEDEC43A',
        # }
        #
        # # 抖音商品
        # url = 'https://api3-normal-c-lq.amemv.com/aweme/v1/promotion/feeds/?version_code=11.1.0&js_sdk_version=1.63.0.6&app_name=aweme&app_version=11.1.0&vid=7DE25B7C-8C79-4E51-8B6F-98E59AA3EDDD&device_id=38763628687&channel=App%20Store&mcc_mnc=46001&aid=1128&screen_width=750&openudid=fb19224c28e96489a071098c581fcb6f167ed2e3&cdid=AC1136FE-C3EA-4029-974D-A4B0CEDEC43A&os_api=18&ac=WIFI&os_version=12.1&build_number=111015&device_platform=iphone&iid=3315770385767840&device_type=iPhone8,1&is_vcd=1&idfa=C6B24C79-AB73-4799-AE9B-3831440859FA&count=20&cursor=0&request_tag_from=rn'
        # headers ={
        #     'Host': 'api3-normal-c-lq.amemv.com',
        #     'Connection': 'keep-alive',
        #     'x-Tt-Token': '004eb26b34a9f979ac9afe25e78fd14e8fccd58c92ad422cdc40e7d0366de60b7e2a9d0fb2ccea7ab2c330aa698d6ab21320',
        #     'sdk-version': '1',
        #     'User-Agent': 'Aweme 11.1.0 rv:111015 (iPhone; iOS 12.1; zh_CN) Cronet',
        #     'X-SS-DP': '1128',
        #     'x-tt-trace-id': '00-2eb4a7c6099067e088f42ee67d640468-2eb4a7c6099067e0-01',
        #     'Accept-Encoding': 'gzip, deflate, br',
        #     'Cookie': 'install_id=3315770385767840; ttreq=1$1d6cca335eb21220eb05e1f9c9f288f3ee1124a1; passport_csrf_token=3210612bf1f16a56d3b945c982d12d19; d_ticket=2114e2fcc7e67612b067bc6e262756980558b; odin_tt=90a4a743659435c28331be7d526f8d0dae41cf51c2e108c312733bf757eedbea7aac4030e4215380e6c071a44df4da69; sid_guard=4eb26b34a9f979ac9afe25e78fd14e8f%7C1598511320%7C5184000%7CMon%2C+26-Oct-2020+06%3A55%3A20+GMT; uid_tt=2f6bb2d4af3b3890236ed38dcbb45b37; uid_tt_ss=2f6bb2d4af3b3890236ed38dcbb45b37; sid_tt=4eb26b34a9f979ac9afe25e78fd14e8f; sessionid=4eb26b34a9f979ac9afe25e78fd14e8f; sessionid_ss=4eb26b34a9f979ac9afe25e78fd14e8f',
        #     'X-Khronos': '1598511424',
        #     'X-Gorgon': '8402205a000031a9b5b82334a2408d08f3d0aa273d76c2cbb91d',
        # }
        #
        # # er
        # url = 'https://api3-normal-c.amemv.com/aweme/v1/promotion/feeds?version_code=11.1.0&js_sdk_version=1.63.0.6&app_name=aweme&app_version=11.1.0&vid=7DE25B7C-8C79-4E51-8B6F-98E59AA3EDDD&device_id=38763628687&channel=App%20Store&mcc_mnc=46001&aid=1128&screen_width=750&openudid=fb19224c28e96489a071098c581fcb6f167ed2e3&cdid=AC1136FE-C3EA-4029-974D-A4B0CEDEC43A&os_api=18&ac=WIFI&os_version=12.1&build_number=111015&device_platform=iphone&iid=3315770385767840&device_type=iPhone8,1&is_vcd=1&idfa=C6B24C79-AB73-4799-AE9B-3831440859FA&count=20&cursor=40&request_tag_from=rn'
        # headers = {
        #     'Host':'api3-normal-c-lq.amemv.com',
        #     'Connection':'keep-alive',
        #     'x-Tt-Token':'004eb26b34a9f979ac9afe25e78fd14e8fccd58c92ad422cdc40e7d0366de60b7e2a9d0fb2ccea7ab2c330aa698d6ab21320',
        #     'sdk-version':'1',
        #     'User-Agent':'Aweme 11.1.0 rv:111015 (iPhone; iOS 12.1; zh_CN) Cronet',
        #     'X-SS-DP':'1128',
        #     'x-tt-trace-id':'00-2eed41dd099067e088f15765cef20468-2eed41dd099067e0-01',
        #     'Accept-Encoding':'gzip, deflate, br',
        #     'Cookie':'passport_csrf_token=3210612bf1f16a56d3b945c982d12d19; d_ticket=2114e2fcc7e67612b067bc6e262756980558b; odin_tt=90a4a743659435c28331be7d526f8d0dae41cf51c2e108c312733bf757eedbea7aac4030e4215380e6c071a44df4da69; sessionid=4eb26b34a9f979ac9afe25e78fd14e8f; sessionid_ss=4eb26b34a9f979ac9afe25e78fd14e8f; sid_guard=4eb26b34a9f979ac9afe25e78fd14e8f%7C1598511320%7C5184000%7CMon%2C+26-Oct-2020+06%3A55%3A20+GMT; sid_tt=4eb26b34a9f979ac9afe25e78fd14e8f; uid_tt=2f6bb2d4af3b3890236ed38dcbb45b37; uid_tt_ss=2f6bb2d4af3b3890236ed38dcbb45b37; install_id=3315770385767840; ttreq=1$1d6cca335eb21220eb05e1f9c9f288f3ee1124a1',
        #     'X-Khronos':'1598515133',
        #     'X-Gorgon':'840260a900005f953229d75fa0888518253fb3943ccf9ea038be',
        # }

        # headers = {
        #     'Host': 'search-hl.amemv.com',
        #     'Connection': 'keep-alive',
        #     'x-Tt-Token': '00394cd35500eb8ab3aa53594effe24e07eba7814da7e2dec73bdce19f24e787d0ea7b556e0d06970b7900cd9274fadea040',
        #     'sdk-version': '1',
        #     'User-Agent': 'Aweme 11.1.0 rv:111015 (iPhone; iOS 12.1; zh_CN) Cronet',
        #     'X-SS-DP': '1128',
        #     'x-tt-trace-id': '00-2449f6f2099067e088f36ccadada0468-2449f6f2099067e0-01',
        #     'Accept-Encoding': 'deflate, br',
        #     'Cookie': 'd_ticket=332d257b0d9915e3baab26354d4904850558b; odin_tt=e72de93f38c19bc4b446b684d5084307be39f2623bdf2896a7a72c2b82a111d13da68ff99d7e1c2f69f329ea550bf1f1; sessionid=394cd35500eb8ab3aa53594effe24e07; sessionid_ss=394cd35500eb8ab3aa53594effe24e07; sid_guard=394cd35500eb8ab3aa53594effe24e07%7C1598260898%7C5184000%7CFri%2C+23-Oct-2020+09%3A21%3A38+GMT; sid_tt=394cd35500eb8ab3aa53594effe24e07; uid_tt=3c0ac05f4f520d1ae76d79f89e784e0f; uid_tt_ss=3c0ac05f4f520d1ae76d79f89e784e0f; install_id=3315770385767840; ttreq=1$1d6cca335eb21220eb05e1f9c9f288f3ee1124a1; passport_csrf_token=caea52df3a45d79a3b4cf3c0ab961675',
        #     'X-Khronos': '1598336660',
        #     'X-Gorgon': '8402009d00007074c6192454c87e40be71114b59193433253dd6',
        #     'x-common-params-v2': 'channel=App%20Store&version_code=11.1.0&app_name=aweme&vid=7DE25B7C-8C79-4E51-8B6F-98E59AA3EDDD&app_version=11.1.0&mcc_mnc=46001&device_id=38763628687&aid=1128&screen_width=750&openudid=fb19224c28e96489a071098c581fcb6f167ed2e3&os_api=18&os_version=12.1&device_platform=iphone&build_number=111015&device_type=iPhone8,1&iid=3315770385767840&idfa=C6B24C79-AB73-4799-AE9B-3831440859FA&js_sdk_version=1.63.0.6&cdid=AC1136FE-C3EA-4029-974D-A4B0CEDEC43A',
        # }
        # url = 'search-hl.amemv.com/aweme/v1/search/item/?ac=WIFI&is_vcd=1&source=video_search&offset=0&search_soruce=normal_search&is_filter_search=0&publish_time=0&count=12&hot_search=0&keyword=%E7%94%B5%E5%8A%A8%E7%89%99%E5%88%B7&sort_type=0&query_correct_type=1'

        # url = 'https://api5-normal-c-lq.amemv.com/aweme/v1/promotion/feeds/?version_code=11.1.0&js_sdk_version=1.63.0.6&app_name=aweme&app_version=11.1.0&vid=7DE25B7C-8C79-4E51-8B6F-98E59AA3EDDD&device_id=38763628687&channel=App%20Store&mcc_mnc=46001&aid=1128&screen_width=750&count=60&cursor={}&category_id=11&request_tag_from=rn'
        # 2精品女装，9新奇特，14宠物用品，
        # 4食品饮料
        # 8京东，10唯品会，
        # url = 'https://api3-normal-c-hl.amemv.com/aweme/v1/promotion/feeds/?version_code=12.4.0&js_sdk_version=1.75.0.9&tma_jssdk_version=1.75.0.9&app_name=aweme&app_version=12.4.0&vid=7DE25B7C-8C79-4E51-8B6F-98E59AA3EDDD&device_id=38763628687&channel=App%20Store&mcc_mnc=46001&aid=1128&screen_width=750&openudid=fb19224c28e96489a071098c581fcb6f167ed2e3&cdid=AC1136FE-C3EA-4029-974D-A4B0CEDEC43A&os_api=18&ac=WIFI&os_version=12.1&build_number=124013&device_platform=iphone&device_type=iPhone8,1&is_vcd=1&iid=2796766574157116&idfa=C6B24C79-AB73-4799-AE9B-3831440859FA&count=20&cursor=0&request_tag_from=rn'
        #
        # headers = {
        #     'Host': 'api3-normal-c-hl.amemv.com',
        #     'Connection': 'keep-alive',
        #     'sdk-version': '2',
        #     'passport-sdk-version': '5.12.1',
        #     'x-Tt-Token': '00f15dff1d5549e9278cc525b037e88908b72cf3e21e57201b89512baa79b6919ad48cb9558906a10a6d033d6b09d7e9f327',
        #     'User-Agent': 'Aweme 12.4.0 rv:124013 (iPhone; iOS 12.1; zh_CN) Cronet',
        #     'X-SS-DP': '1128',
        #     'x-tt-trace-id': '00-51cb6dc1099067e088ffe62badc90468-51cb6dc1099067e0-01',
        #     'Accept-Encoding': 'gzip, deflate, br',
        #     'Cookie': 'install_id=2796766574157116; ttreq=1$0b5e3737f04ff7993ba52ff5c1dbd271de6e0d72; passport_csrf_token=bdd81c6a73483d43983a934a3625e7a0; d_ticket=2114e2fcc7e67612b067bc6e262756980558b; multi_sids=78444018342%3Af15dff1d5549e9278cc525b037e88908; odin_tt=babd253946e0e44271d22a14a2543593ccc9b18e69f631589afbdd7a4803a5742f00a8d4b05d6038e23069b14dba23a7; sid_guard=f15dff1d5549e9278cc525b037e88908%7C1599099766%7C5184000%7CMon%2C+02-Nov-2020+02%3A22%3A46+GMT; uid_tt=b50b196a61fc3691e12695cb2deab6d7; uid_tt_ss=b50b196a61fc3691e12695cb2deab6d7; sid_tt=f15dff1d5549e9278cc525b037e88908; sessionid=f15dff1d5549e9278cc525b037e88908; sessionid_ss=f15dff1d5549e9278cc525b037e88908',
        #     'X-Khronos': '1599100119',
        #     'X-Gorgon': '8402806c0000c6ac804efb1911ff8d47c3d25d42d90887d327ef',
        # }
        # for i in  list(range(0,10000,20)):
        #
        #     while True:
        #         print(i)
        #         try:
        #             status, response = await async_http_response(url.format(i), headers=headers)
        #             print(response)
        #             data_dict = json.loads(response)
        #             # print(data_dict)
        #             for i in data_dict['promotions']:
        #
        #                 # print(i['promotion_id'])
        #                 print(i['title'])
        #                 print(i)
        #             break
        #         except Exception as e:
        #             continue

        # url = 'https://pub.alimama.com/cp/event/list.json?toPage=1&perPageSize=40&status=7&sceneId=6&t=1599025299317&_tb_token_=e557b3ee9d686&pvid='
        # headers = {
        #     'Accept': 'application/json, text/javascript, */*; q=0.01',
        #     'Accept-Encoding': 'gzip, deflate, br',
        #     'Accept-Language': 'zh-CN,zh;q=0.9',
        #     'Connection': 'keep-alive',
        #     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        #     'Cookie': 't=e14148ad9694b3451771bdaff276f7c1; cookie2=1c140359394b15294c0f316d0c625972; _tb_token_=e557b3ee9d686; cna=LyyhFyc44A0CARuaTgVR/hHQ; xlly_s=1; account-path-guide-s1=true; x5sec=7b22756e696f6e2d7075623b32223a223938633630386239376664353665383264353765616230396634363434346461434a486576506f4645497a30352f694f733757447441453d227d; v=0; alimamapwag=TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzg0LjAuNDE0Ny4xMzUgU2FmYXJpLzUzNy4zNg%3D%3D; cookie32=eecee0d30a895e5a9b125bdac7c2984e; alimamapw=ESYmFXUNFHtyFHpxQ3oFRnNXESZVFXMNOAkBVQ0DBw4CU1NWA1xXU1cJUgoDAgpXVw4EBQVSUAAH%0A; cookie31=MzIwMDMyMDksJUU2JUI3JTk4JUU1JUFFJUEyJUU2JTlEJUE1JUU2JTlEJUE1LDk2MzczOUBxcS5jb20sVEI%3D; login=URm48syIIVrSKA%3D%3D; JSESSIONID=14A5356C5F137BB6FDA250195811DE04; tfstk=cmYhBObZSHSICvjMc2_BGFqI7vxlZlZFHU-27Fx2Zz_OVMTNi6Ea0DNKs_pHyu1..; l=eBPCOxYqOs527wfwXOfwlurza77OAIRAguPzaNbMiOCP9z1W54qcWZP3-v8XCnGVh6VvR3-WSGYuBeYBqIDs1YkV6O0WdpMmn; isg=BJSUT4UItwiakiPEzvwdZ5hpZdIG7bjXYg_E_y51D5-iGTRjVvzUZgKfGRGB4fAv',
        #     'Host': 'pub.alimama.com',
        #     'Referer': 'https://pub.alimama.com/manage/cpevent/index.htm?spm=a219t.11817064.1998910419.dd412374a3.330075a5nYg6KI',
        #     'Sec-Fetch-Dest': 'empty',
        #     'Sec-Fetch-Mode': 'cors',
        #     'Sec-Fetch-Site': 'same-origin',
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
        #     'X-Requested-With': 'XMLHttpRequest',
        # }
        # res= []
        # status, response = await async_http_response(url, headers=headers)
        # data_dict = json.loads(response)
        # print(1,data_dict)
        # for item in data_dict['data']['result']:
        #     print(item['eventId'])
        #     eventId=item['eventId']
        #     the_url = 'https://pub.alimama.com/cp/event/item/list.json?eventId={}&category=&auditorId=&auditStatus=&keyword=&toPage=1&perPageSize=40&t=1599024939033&_tb_token_=e557b3ee9d686&pvid='.format(eventId)
        #     headers = {
        #         'Accept': 'application/json, text/javascript, */*; q=0.01',
        #         'Accept-Encoding': 'gzip, deflate, br',
        #         'Accept-Language': 'zh-CN,zh;q=0.9',
        #         'Connection': 'keep-alive',
        #         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        #         'Cookie': 't=e14148ad9694b3451771bdaff276f7c1; cookie2=1c140359394b15294c0f316d0c625972; v=0; _tb_token_=e557b3ee9d686; cna=LyyhFyc44A0CARuaTgVR/hHQ; alimamapwag=TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzg0LjAuNDE0Ny4xMzUgU2FmYXJpLzUzNy4zNg%3D%3D; cookie32=eecee0d30a895e5a9b125bdac7c2984e; alimamapw=ESYmFXUNFHtyFHpxQ3oFRnNXESZVFXMNOAkBVQ0DBw4CU1NWA1xXU1cJUgoDAgpXVw4EBQVSUAAH%0A; cookie31=MzIwMDMyMDksJUU2JUI3JTk4JUU1JUFFJUEyJUU2JTlEJUE1JUU2JTlEJUE1LDk2MzczOUBxcS5jb20sVEI%3D; xlly_s=1; account-path-guide-s1=true; login=URm48syIIVrSKA%3D%3D; x5sec=7b22756e696f6e2d7075623b32223a223938633630386239376664353665383264353765616230396634363434346461434a486576506f4645497a30352f694f733757447441453d227d; JSESSIONID=B15CA1495CD4F99100C79F08C40CB027; l=eBPCOxYqOs527zYaBOfwourza77OSIRAguPzaNbMiOCP911y5DvOWZP3Dg82C3GVhsiJR3-WSGYuBeYBqIVjE4w89F4Le8Hmn; tfstk=ctW5BptR240WRaVEUgZ28gj4D6vlZ10XY7tdV_wjGM_S1ej5i9Dw5noltVDv6n1..; isg=BJOTy1pVyPX-J4ShJXkSChOUIhe9SCcKecLj2kWw77LpxLNmzRi3WvES_jSq5H8C',
        #         'Host': 'pub.alimama.com',
        #         'Referer': 'https://pub.alimama.com/manage/cpevent/index.htm?spm=a219t.11817064.1998910419.dd412374a3.330075a5nYg6KI',
        #         'Sec-Fetch-Dest': 'empty',
        #         'Sec-Fetch-Mode': 'cors',
        #         'Sec-Fetch-Site': 'same-origin',
        #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
        #         'X-Requested-With': 'XMLHttpRequest',
        #     }
        #     status, response = await async_http_response(the_url, headers=headers)
        #     data_dict = json.loads(response)
        #     print('data_dict',data_dict)
            # res.append(data_dict)
        # 评论
        url='https://api3-normal-c-hl.amemv.com/aweme/v2/shop/promotion/comments/?version_code=12.4.0&js_sdk_version=1.75.0.9&tma_jssdk_version=1.75.0.9&app_name=aweme&app_version=12.4.0&vid=7DE25B7C-8C79-4E51-8B6F-98E59AA3EDDD&device_id=38763628687&channel=App%20Store&mcc_mnc=46001&aid=1128&screen_width=750&openudid=fb19224c28e96489a071098c581fcb6f167ed2e3&cdid=AC1136FE-C3EA-4029-974D-A4B0CEDEC43A&os_api=18&ac=WIFI&os_version=12.1&build_number=124013&device_platform=iphone&device_type=iPhone8,1&is_vcd=1&iid=2796766574157116&idfa=C6B24C79-AB73-4799-AE9B-3831440859FA&product_id=3428852898849772840&cursor=0&count=10&stat_id=2'
        headers={
            'Host': 'api3-normal-c-hl.amemv.com',
            'Connection': 'keep-alive',
            'sdk-version': '2',
            'passport-sdk-version': '5.12.1',
            'x-Tt-Token': '00f15dff1d5549e9278cc525b037e88908b72cf3e21e57201b89512baa79b6919ad48cb9558906a10a6d033d6b09d7e9f327',
            'User-Agent': 'Aweme 12.4.0 rv:124013 (iPhone; iOS 12.1; zh_CN) Cronet',
            'X-SS-DP': '1128',
            'x-tt-trace-id': '00-56cb6530099067e088fe0723bb710468-56cb6530099067e0-01',
            'Accept-Encoding': 'gzip, deflate, br',
            # 'Cookie': 'd_ticket=2114e2fcc7e67612b067bc6e262756980558b; multi_sids=78444018342%3Af15dff1d5549e9278cc525b037e88908; odin_tt=babd253946e0e44271d22a14a2543593ccc9b18e69f631589afbdd7a4803a5742f00a8d4b05d6038e23069b14dba23a7; sessionid=f15dff1d5549e9278cc525b037e88908; sessionid_ss=f15dff1d5549e9278cc525b037e88908; sid_guard=f15dff1d5549e9278cc525b037e88908%7C1599099766%7C5184000%7CMon%2C+02-Nov-2020+02%3A22%3A46+GMT; sid_tt=f15dff1d5549e9278cc525b037e88908; uid_tt=b50b196a61fc3691e12695cb2deab6d7; uid_tt_ss=b50b196a61fc3691e12695cb2deab6d7; install_id=2796766574157116; ttreq=1$0b5e3737f04ff7993ba52ff5c1dbd271de6e0d72',
            # 'X-Khronos': '1599184003',
            # 'X-Gorgon': '8402802f0000ef02d0a0003127df8090ef64e0d7d63590c0a03a',
        }
        status, response = await async_http_response(url, headers=headers)
        data_dict = json.loads(response)
        print('data_dict',data_dict)
        return self.send_message(True, 0, 'success',data_dict )
        # self.write('login')



if __name__ == '__main__':
    pass
