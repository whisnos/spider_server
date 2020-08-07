import datetime
import operator
import threading

from asgiref.sync import sync_to_async

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

    def return_data(self, collection, item, now_prv, now):
        data_dict = {}
        print('item', item, now_prv)
        the_data = []
        for doc in collection.find({"itemid": str(item), "createTime": {"$gte": now_prv, "$lte": now}}):
            # doc.pop('_id', '404')
            # doc.pop('createTime', '404')

            print('doc', doc)
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

    async def post(self, *args, **kwargs):
        self.result = []
        items = self.verify_arg_legal(self.get_body_argument('items'), '商品id')
        now = datetime.datetime.now()
        now_prv = datetime.datetime.now() - datetime.timedelta(hours=2)
        # now_prv = now - datetime.timedelta(hours=24 * 7) - datetime.timedelta(hours=now.hour, minutes=now.minute,
        #                                                                       seconds=now.second,
        #                                                                       microseconds=now.microsecond)
        # day = now.day
        day = str(now_prv.date()).replace('-', '_')
        item_list = items.split(',')
        # collection = eval('self.db.products_{}'.format(day))
        print('day', day)
        collection = eval('db.products_{}'.format(day))
        # collection = eval('self.db.product_{}'.format(21))
        result = []
        for item in item_list:
            data_dict = {}
            the_data = []
            async for doc in collection.find({"itemid": str(item), "createTime": {"$gte": now_prv, "$lte": now}}):
                # doc.pop('_id', '404')
                # doc.pop('createTime', '404')
                the_data.append(doc)
            if the_data:
                the_num = int(the_data[-1]['volume']) - int(the_data[0]['volume'])
                volume = the_num if the_num >= 0 else 0
                data_dict['itemid'] = item
                data_dict['volume'] = volume
                result.append(data_dict)
            else:
                data_dict['itemid'] = item
                data_dict['volume'] = 0
                result.append(data_dict)
        # size = 20
        # for b in [item_list[i:i + size] for i in range(0, len(item_list), size)]:
        #     threads = []
        #     for u in b:
        #         t = threading.Thread(target=self.return_data, args=(collection, u, now_prv, now))
        #         t.start()
        #         threads.append(t)
        #     for t in threads:
        #         t.join()
        print('主进程结束')
        return self.send_message(True, 0, 'success', result)


class CountUserProductSellHandler(BaseHandler):

    async def do_find_one(self, this_day, TmID):
        this_day_collection = eval('db.products_{}'.format(this_day))
        print(6)
        async for document in this_day_collection.find({"itemid": str(TmID)}):
            print(123, document)

    async def post(self, *args, **kwargs):
        user_id = self.verify_arg_legal(self.get_body_argument('userid'), '商家id')
        the_type = self.verify_arg_num(self.get_body_argument('type'), '类型', is_num=True)
        cur, conn = return_sqlserver_connect()
        search_item_sql = "select TmID,Name from Product where User_ID='{}'".format(user_id)
        print('search_item_sql', search_item_sql, the_type)
        if not cur:
            return self.send_message(False, 400, '连接失败', None)
        try:
            cur.execute(search_item_sql)
            the_results = cur.fetchall()
            conn.commit()
        except Exception as e:
            return self.send_message(False, 400, '获取失败', None)
        # 处理时间
        all_day = []
        print(666, len(the_results))
        for i in range(the_type):  # 1,the_type+1
            data_dict = {}
            the_day = (datetime.datetime.now() - datetime.timedelta(hours=i * 24)).date()
            this_day = str((datetime.datetime.now() - datetime.timedelta(hours=i * 24)).date()).replace('-', '_')
            # data_dict 每天的数据统计
            data_dict['day'] = str(the_day)
            data_dict['volume'] = 0
            print(888, the_results[0], this_day)
            for item in the_results:
                # await self.do_find_one(this_day,item["TmID"])
                the_data = []
                this_day_collection = eval('db.products_{}'.format(this_day))
                # print('11',item["TmID"],this_day_collection.find({"itemid": str(item["TmID"])}))
                try:
                    async for doc in this_day_collection.find({"itemid": str(item["TmID"])}).sort('createTime',
                                                                                                  1).limit(1):
                        # print('doc第一',doc,)
                        the_data.append(doc)
                    async for doc in this_day_collection.find({"itemid": str(item["TmID"])}).sort('createTime',
                                                                                                  -1).limit(1):
                        # print('doc最后',doc,)
                        the_data.append(doc)
                    if the_data:
                        the_num = int(the_data[-1]['volume']) - int(the_data[0]['volume'])
                        volume = the_num if the_num >= 0 else 0
                    else:
                        volume = 0
                    data_dict['volume'] = data_dict['volume'] + volume
                except Exception as e:
                    print('异常', e)
                    return self.send_message(False, 400, '异常', None)
            all_day.append(data_dict)
        return self.send_message(True, 0, 'success', all_day)


class CountProductTopSellHandler(BaseHandler):
    async def post(self, *args, **kwargs):
        cate_id = self.verify_arg_legal(self.get_body_argument('cate_id', ''), '类目id')
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
            # print(i)
        # cursor_min = collection.aggregate([min_dict])
        async for i in cursor_min:
            # the_dict = {}
            # the_dict['min'] = i['volume']
            data_dict[i['_id']]['min'] = i['volume']
            # print(i)
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
        cate_id = self.verify_arg_legal(self.get_body_argument('cate_id',''), '类目id')
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
            max_list.insert(0,cate_dict)
            min_list.insert(0,cate_dict)

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
