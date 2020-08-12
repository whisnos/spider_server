import datetime
import operator
import threading

from asgiref.sync import sync_to_async
from tornado import queues, gen

from config import MONGODB
from tool.function import return_sqlserver_connect
from webhandler.basehandler import BaseHandler
import pymssql

# conn = pymssql.connect(host='192.168.32.24', port='1433', user='sa', password='shanpengfei@no1', database='TaoKe')
# cur = conn.cursor()
from pymongo import MongoClient

# client = MongoClient('127.0.0.1', 27017)
from motor.motor_asyncio import AsyncIOMotorClient

# client = AsyncIOMotorClient('mongodb://testmongo:testmongo123@39.105.179.250:27017/spider')
client = AsyncIOMotorClient(
    'mongodb://{}:{}@{}:{}/{}'.format(MONGODB['user'], MONGODB['pwd'], MONGODB['host'], MONGODB['port'],
                                      MONGODB['db'], ))
# client = MongoClient('39.105.179.250', 27017)
db = client.spider


# db.authenticate('testmongo', 'testmongo123')


class CountProductSellHandler(BaseHandler):

    async def return_data(self,item):
        data_dict = {}
        the_data = []
        async for doc in self.collection.find({"itemid": str(item), "createTime": {"$gte": self.now_prv, "$lte": self.now}}):
            # doc.pop('_id', '404')
            # doc.pop('createTime', '404')
            the_data.append(doc)
        if the_data:
            the_num = int(the_data[-1]['volume']) - int(the_data[0]['volume'])
            volume = the_num if the_num >= 0 else 0
            data_dict['itemid'] = item
            data_dict['volume'] = volume
            self.result.append(data_dict)
        else:
            data_dict['itemid'] = item
            data_dict['volume'] = 0
            self.result.append(data_dict)
    async def worker(self):
        async for url in self.q:
            # async for 这边是不会退出的，所以 需要下面这句 进行return退出
            if url is None:
                return
            # print('更新...', url)
            try:
                await self.return_data(url)
            except Exception as e:
                print(f"exception:{e}")
            finally:
                # print("X................", count)
                # 计数器，每put进入一个就加1，所以我们调用完了之后，要减去1
                self.q.task_done()
    async def post(self, *args, **kwargs):
        self.result = []
        items = self.verify_arg_legal(self.get_body_argument('items'), '商品id')
        self.now = datetime.datetime.now()
        self.now_prv = datetime.datetime.now() - datetime.timedelta(hours=2)
        # now_prv = now - datetime.timedelta(hours=24 * 7) - datetime.timedelta(hours=now.hour, minutes=now.minute,
        #                                                                       seconds=now.second,
        #                                                                       microseconds=now.microsecond)
        # day = now.day
        day = str(self.now_prv.date()).replace('-', '_')
        item_list = items.split(',')
        # collection = eval('self.db.products_{}'.format(day))
        print('day', day)
        self.collection = eval('db.products_{}'.format(day))
        # collection = eval('self.db.product_{}'.format(21))
        # result = []

        self.q = queues.Queue()
        for item in item_list:
            await self.q.put(item)
        workers = gen.multi([self.worker() for _ in range(10)])

        # 会阻塞，直到队列里面没有数据为止
        await self.q.join()
        print("join")
        for _ in range(10):
            # 放入相应的None数量 以至协程退出
            await self.q.put(None)
        print("None...")

        # 等待所有协程执行完毕
        await workers
        # for item in item_list:
        #     data_dict = {}
        #     the_data = []
        #     async for doc in collection.find({"itemid": str(item), "createTime": {"$gte": now_prv, "$lte": now}}):
        #         # doc.pop('_id', '404')
        #         # doc.pop('createTime', '404')
        #         the_data.append(doc)
        #     if the_data:
        #         the_num = int(the_data[-1]['volume']) - int(the_data[0]['volume'])
        #         volume = the_num if the_num >= 0 else 0
        #         data_dict['itemid'] = item
        #         data_dict['volume'] = volume
        #         result.append(data_dict)
        #     else:
        #         data_dict['itemid'] = item
        #         data_dict['volume'] = 0
        #         result.append(data_dict)
        print('主进程结束')
        return self.send_message(True, 0, 'success', self.result)


class CountUserProductSellHandler(BaseHandler):

    async def post(self, *args, **kwargs):
        user_id = self.verify_arg_legal(self.get_body_argument('userid'), '商家id')
        the_type = self.verify_arg_num(self.get_body_argument('type','7'), '类型', is_num=True)
        result = []
        async for doc in db.users_sell.find({"ID": user_id.lower()}).sort([("_id", -1)]).limit(the_type):
            doc.pop('_id', '404')
            doc.pop('ID', '404')
            doc.pop('createTime', '404')
            result.append(doc)
        return self.send_message(True, 0, 'success', result)


class CountProductTopSellHandler(BaseHandler):
    async def post(self, *args, **kwargs):
        cate_id = self.verify_arg_legal(self.get_body_argument('cate_id', ''), '类目id')
        user_id = self.verify_arg_legal(self.get_body_argument('user_id', ''), '类目id')
        if user_id and cate_id:
            return self.send_message(False, 0, '参数错误', [])
        now = datetime.datetime.now()
        day = now.date()
        day_format = str(day).replace('-', '_')
        # from pymongo import MongoClient
        # client = MongoClient('39.105.179.250', 27017)
        # db = client.spider
        # db.authenticate('testmongo', 'testmongo123')
        collection = eval('db.products_{}'.format(day_format))

        # collection.aggregate([{"$group": {"itemid": "$itemid", "num": {"$sum": "$likes"}}}])
        max_list = []
        min_list = []
        if not cate_id:
            # cate_dict = {"$match":{"cateid": "$cateid"}}
            pass
        else:
            cate_dict = {"$match": {"cateid": cate_id}}
            max_list.insert(0, cate_dict)
            min_list.insert(0, cate_dict)

        if not user_id:
            # cate_dict = {"$match":{"cateid": "$cateid"}}
            pass
        else:
            cate_dict = {"$match": {"userid": user_id}}
            max_list.insert(0, cate_dict)
            min_list.insert(0, cate_dict)

        max_dict = {"$group": {"_id": "$itemid", "volume": {"$last": "$volume"}}}
        max_list.append(max_dict)
        min_dict = {"$group": {"_id": "$itemid", "volume": {"$first": "$volume"}}}
        min_list.append(min_dict)
        cursor_max = await sync_to_async(collection.aggregate)(max_list)
        cursor_min = await sync_to_async(collection.aggregate)(min_list)
        # async for a in cursor_max:
        #     print(1111111,a)
        # the_dict = {"$group": {"_id":"$itemid","volume":{"$sum":{ "$multiply": [ "$price", "$quantity" ] }}}}

        # cursor_max = collection.aggregate([max_dict])
        data_dict = {}
        async for i in cursor_max:
            the_dict = {}
            the_dict['max'] = i['volume']
            data_dict[i['_id']] = the_dict
        # cursor_min = collection.aggregate([min_dict])
        async for i in cursor_min:
            # the_dict = {}
            # the_dict['min'] = i['volume']
            data_dict[i['_id']]['min'] = i['volume']

        print('data_dict')
        result = []
        for k, v in data_dict.items():
            # print(k,v)
            the_sub = []
            for a, b in v.items():
                the_sub.append(b)
            data = int(the_sub[0]) - int(the_sub[1])
            return_data = {}
            return_data['itemid'] = k
            return_data['volume'] = data
            result.append(return_data)
        new_list = sorted(result, key=operator.itemgetter('volume'), reverse=True)[:100]
        return self.send_message(True, 0, 'success', new_list)


class CountProductHourTopSellHandler(BaseHandler):
    async def post(self, *args, **kwargs):
        cate_id = self.verify_arg_legal(self.get_body_argument('cate_id', ''), '类目id')
        now = datetime.datetime.now()
        day = now.date()
        day_format = str(day).replace('-', '_')
        two_hour = now - datetime.timedelta(hours=2)
        print('two_hour', two_hour)
        # from pymongo import MongoClient
        # client = MongoClient('39.105.179.250', 27017)
        # db = client.spider
        # db.authenticate('testmongo', 'testmongo123')
        collection = eval('db.products_{}'.format(day_format))

        # collection.aggregate([{"$group": {"itemid": "$itemid", "num": {"$sum": "$likes"}}}])
        max_list = []
        min_list = []
        if not cate_id:
            # cate_dict = {"$match":{"cateid": "$cateid"}}
            pass
        else:
            cate_dict = {"$match": {"cateid": cate_id}}
            max_list.insert(0, cate_dict)
            min_list.insert(0, cate_dict)

        sec_dict = {"$match": {"createTime": {"$lte": two_hour}}}
        min_list.append(sec_dict)
        max_dict = {"$group": {"_id": "$itemid", "volume": {"$last": "$volume"}}}
        max_list.append(max_dict)

        min_dict = {"$group": {"_id": "$itemid", "volume": {"$last": "$volume"}}}
        min_list.append(min_dict)
        # sec_dict = {"$skip" : 3}

        # print('max_list',max_list)
        # print('min_list',min_list)
        cursor_max = await sync_to_async(collection.aggregate)(max_list)
        cursor_min = await sync_to_async(collection.aggregate)(min_list)
        # async for a in cursor_max:
        #     print(1111111,a)
        # the_dict = {"$group": {"_id":"$itemid","volume":{"$sum":{ "$multiply": [ "$price", "$quantity" ] }}}}

        # cursor_max = collection.aggregate([max_dict])
        data_dict = {}
        async for i in cursor_max:
            the_dict = {}
            the_dict['max'] = i['volume']
            data_dict[i['_id']] = the_dict
            # print('max',i)
        # cursor_min = collection.aggregate([min_dict])
        async for i in cursor_min:
            # the_dict = {}
            # the_dict['min'] = i['volume']
            data_dict[i['_id']]['min'] = i['volume']
            # print('min',i)
        # print('data_dict',data_dict)
        result = []
        for k, v in data_dict.items():
            # print(k,v)
            the_sub = []
            for a, b in v.items():
                the_sub.append(b)
            data = int(the_sub[0]) - int(the_sub[-1])
            return_data = {}
            return_data['itemid'] = k
            return_data['volume'] = data
            result.append(return_data)
        new_list = sorted(result, key=operator.itemgetter('volume'), reverse=True)[:100]
        return self.send_message(True, 0, 'success', new_list)


# class CountProductCateTopSellHandler(BaseHandler):
#     async def post(self, *args, **kwargs):
#         cate_id = self.verify_arg_legal(self.get_body_argument('cate_id'), '类目id')
#         now = datetime.datetime.now()
#         day = now.date()
#         day_format = str(day).replace('-', '_')
#         collection = eval('db.products_{}'.format(day_format))
#         max_dict = {"$group": {"_id": "$itemid", "volume": {"$last": "$volume"}}}
#         min_dict = {"$group": {"_id": "$itemid", "volume": {"$first": "$volume"}}}
#         sec_dict = {"$match": {"cateid": cate_id}}
#         cursor_max = await sync_to_async(collection.aggregate)([sec_dict,max_dict])
#         cursor_min = await sync_to_async(collection.aggregate)([sec_dict, min_dict, ])
#         data_dict = {}
#         async for i in cursor_max:
#             the_dict = {}
#             the_dict['max'] = i['volume']
#             data_dict[i['_id']] = the_dict
#         async for i in cursor_min:
#             data_dict[i['_id']]['min'] = i['volume']
#         result = []
#         for k, v in data_dict.items():
#             the_sub = []
#             for a, b in v.items():
#                 the_sub.append(b)
#             data = int(the_sub[0]) - int(the_sub[1])
#             return_data = {}
#             return_data['itemid'] = k
#             return_data['volume'] = data
#             result.append(return_data)
#         new_list = sorted(result, key=operator.itemgetter('volume'), reverse=True)[:100]
#         return self.send_message(True, 0, 'success', new_list)


if __name__ == '__main__':
    pass
