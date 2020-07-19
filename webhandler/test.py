import tornado.web
from tool.dbpool import DbOperate
from tool.async_redis_pool import RedisOperate
from sms.aliyunsms import send_aliyun_send_sms
from webhandler.basehandler import BaseHandler, check_login
from tool import applog, function
from config import TOKEN_TIME, SMS_VERIFY_TIME, SMS_TEMPLATE_DICT
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
    async def get(self):
        result = []
        data = {
            'id': 1,
            'content': '测试'
        }
        # self.db.search_words_dtk.update_one({'id': 1}, {'$set': {'content': '酸辣辣'}})

        print(55)

        async for doc in self.db.search_words_dtk.find().limit(2):
            doc.pop('date', '404')
            doc.pop('_id', '404')
            doc.pop('isis', '404')
            result.append(doc)
        return self.send_message(True, 0, 'success', result)
        # self.write('login')



if __name__ == '__main__':
    pass
    # async def test_user_sendsms():
    #     obj = UserHandler()
    #     await RedisOperate().instance().create_redis_pool()
    #     await DbOperate().instance().create_db_pool()
    #     code, result = await obj.send_sms('1','13950126971')
    #     print(code, result)

    # import asyncio
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(test_user_sendsms())
