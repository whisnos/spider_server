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
        # headers = {
        #     "Host":"api3-core-c-lq.amemv.com",
        #     "Connection":"keep-alive",
        #     "x-Tt-Token":"00394cd35500eb8ab3aa53594effe24e07fa9dc22850258a1de00148dbedb02ca92b87ca3d124996e930122749d9d96ee646",
        #     "sdk-version":"1",
        #     "User-Agent":"Aweme 11.1.0 rv:111015 (iPhone; iOS 12.1; zh_CN) Cronet",
        #     "X-SS-DP":"1128",
        #     "x-tt-trace-id":"00-1056994a099067e088f52ac977e50468-1056994a099067e0-01",
        #     "Accept-Encoding":"gzip, deflate, br",
        #     "Cookie":"d_ticket=332d257b0d9915e3baab26354d4904850558b; odin_tt=e72de93f38c19bc4b446b684d5084307be39f2623bdf2896a7a72c2b82a111d13da68ff99d7e1c2f69f329ea550bf1f1; sessionid=394cd35500eb8ab3aa53594effe24e07; sessionid_ss=394cd35500eb8ab3aa53594effe24e07; sid_guard=394cd35500eb8ab3aa53594effe24e07%7C1596028476%7C5184000%7CSun%2C+27-Sep-2020+13%3A14%3A36+GMT; sid_tt=394cd35500eb8ab3aa53594effe24e07; uid_tt=3c0ac05f4f520d1ae76d79f89e784e0f; uid_tt_ss=3c0ac05f4f520d1ae76d79f89e784e0f; install_id=3315770385767840; ttreq=1$1d6cca335eb21220eb05e1f9c9f288f3ee1124a1",
        #     "X-Khronos":"1598001943",
        #     "X-Gorgon":"8402c00c000015cd7f4a7f360a44985f1e2e22e39a9a6646f386",
        #     "x-common-params-v2":"channel=App%20Store&version_code=11.1.0&app_name=aweme&vid=7DE25B7C-8C79-4E51-8B6F-98E59AA3EDDD&app_version=11.1.0&mcc_mnc=46001&device_id=38763628687&aid=1128&screen_width=750&openudid=fb19224c28e96489a071098c581fcb6f167ed2e3&os_api=18&os_version=12.1&device_platform=iphone&build_number=111015&device_type=iPhone8,1&iid=3315770385767840&idfa=C6B24C79-AB73-4799-AE9B-3831440859FA&js_sdk_version=1.63.0.6&cdid=AC1136FE-C3EA-4029-974D-A4B0CEDEC43A",
        #
        # }
        # url = 'https://api3-core-c-lq.amemv.com/aweme/v1/aweme/post/?ac=WIFI&is_vcd=1&publish_video_strategy_type=2&min_cursor=0&source=0&sec_user_id=MS4wLjABAAAAzcu8wS4HSxpwfzn720ajP2GQD6zn3j-90V9jY1-5QIs&count=21&user_id=97892293947&max_cursor=0&'
        headers={
            "Host": "api3-core-c-lq.amemv.com",
            "Connection": "keep-alive",
            "x-Tt-Token": "00394cd35500eb8ab3aa53594effe24e07fa9dc22850258a1de00148dbedb02ca92b87ca3d124996e930122749d9d96ee646",
            "sdk-version": "1",
            "User-Agent": "Aweme 11.1.0 rv:111015 (iPhone; iOS 12.1; zh_CN) Cronet",
            "X-SS-DP": "1128",
            "x-tt-trace-id": "00-1056a62d099067e088f7c58eb8d20468-1056a62d099067e0-01",
            "Accept-Encoding": "gzip, deflate, br",
            "Cookie": "d_ticket=332d257b0d9915e3baab26354d4904850558b; odin_tt=e72de93f38c19bc4b446b684d5084307be39f2623bdf2896a7a72c2b82a111d13da68ff99d7e1c2f69f329ea550bf1f1; sessionid=394cd35500eb8ab3aa53594effe24e07; sessionid_ss=394cd35500eb8ab3aa53594effe24e07; sid_guard=394cd35500eb8ab3aa53594effe24e07%7C1596028476%7C5184000%7CSun%2C+27-Sep-2020+13%3A14%3A36+GMT; sid_tt=394cd35500eb8ab3aa53594effe24e07; uid_tt=3c0ac05f4f520d1ae76d79f89e784e0f; uid_tt_ss=3c0ac05f4f520d1ae76d79f89e784e0f; install_id=3315770385767840; ttreq=1$1d6cca335eb21220eb05e1f9c9f288f3ee1124a1",
            "X-Khronos": "1598001943",
            "X-Gorgon": "84026026000092b0addcf32d97575652088c05d6d70a934b8d8c",
            "x-common-params-v2": "channel=App%20Store&version_code=11.1.0&app_name=aweme&vid=7DE25B7C-8C79-4E51-8B6F-98E59AA3EDDD&app_version=11.1.0&mcc_mnc=46001&device_id=38763628687&aid=1128&screen_width=750&openudid=fb19224c28e96489a071098c581fcb6f167ed2e3&os_api=18&os_version=12.1&device_platform=iphone&build_number=111015&device_type=iPhone8,1&iid=3315770385767840&idfa=C6B24C79-AB73-4799-AE9B-3831440859FA&js_sdk_version=1.63.0.6&cdid=AC1136FE-C3EA-4029-974D-A4B0CEDEC43A",

        }
        url = 'https://api3-core-c-lq.amemv.com/aweme/v1/aweme/post/?ac=WIFI&is_vcd=1&publish_video_strategy_type=2&min_cursor=0&source=0&sec_user_id=MS4wLjABAAAAqdUhGhZjvXdPxl0qk1_MYkLwPwMQ5_-BhbPjJzzUwb0fykb3OB18QWIjhSflQyYo&count=21&user_id=2576873519073694&max_cursor=0&'
        status, response = await async_http_response(url, headers=headers)
        print(type(response))
        data_dict = json.loads(response)
        print(  (data_dict))
        return self.send_message(True, 0, 'success',data_dict )
        # self.write('login')



if __name__ == '__main__':
    pass
