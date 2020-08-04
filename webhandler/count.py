import datetime
import threading

from tool.function import return_sqlserver_connect
from webhandler.basehandler import BaseHandler
import pymssql

# conn = pymssql.connect(host='192.168.32.24', port='1433', user='sa', password='shanpengfei@no1', database='TaoKe')
# cur = conn.cursor()
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client.spider
db.authenticate('testmongo', 'testmongo123')

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
        # for item in item_list:
        #     data_dict = {}
        #     the_data=[]
        #     async for doc in collection.find({"itemid": str(item), "createTime": {"$gte": now_prv, "$lte": now}}):
        #         # doc.pop('_id', '404')
        #         # doc.pop('createTime', '404')
        #         the_data.append(doc)
        #     if the_data:
        #         the_num = int(the_data[-1]['volume'])-int(the_data[0]['volume'])
        #         volume = the_num if the_num >= 0 else 0
        #         data_dict['itemid']=item
        #         data_dict['volume'] = volume
        #         result.append(data_dict)
        #     else:
        #         data_dict['itemid'] = item
        #         data_dict['volume'] = 0
        #         result.append(data_dict)
        size = 20
        for b in [item_list[i:i + size] for i in range(0, len(item_list), size)]:
            threads = []
            for u in b:
                t = threading.Thread(target=self.return_data, args=(collection, u, now_prv, now))
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
        print('主进程结束')
        return self.send_message(True, 0, 'success', self.result)


class CountUserProductSellHandler(BaseHandler):
    async def post(self, *args, **kwargs):
        user_id = self.verify_arg_legal(self.get_body_argument('userid'), '商家id')
        the_type = self.verify_arg_num(self.get_body_argument('type'), '类型', is_num=True)
        cur, conn = return_sqlserver_connect()
        search_item_sql = "select TmID,Name from Product where User_ID='{}'".format(user_id)
        print('search_item_sql', search_item_sql, the_type)
        if not cur:
            return self.send_message(True, 0, '没有数据', None)
        try:
            cur.execute(search_item_sql)
            the_results = cur.fetchall()
            conn.commit()
        except Exception as e:
            return self.send_message(True, 0, '没有数据', None)
        # 处理时间
        all_day = []
        print(666,len(the_results))
        for i in range(the_type):
            data_dict = {}
            the_day = (datetime.datetime.now() - datetime.timedelta(hours=i * 24)).date()
            this_day = str((datetime.datetime.now() - datetime.timedelta(hours=i * 24)).date()).replace('-', '_')
            # data_dict 每天的数据统计
            data_dict['day'] = str(the_day)
            data_dict['volume'] = 0
            print(888,the_results[0])
            for item in the_results:
                the_data = []
                this_day_collection = eval('db.products_{}'.format(this_day))
                async for doc in this_day_collection.find({"itemid": str(item["TmID"])}):
                    print('doc',doc,item["TmID"])
                    the_data.append(doc)
                if the_data:
                    the_num = int(the_data[-1]['volume']) - int(the_data[0]['volume'])
                    volume = the_num if the_num >= 0 else 0
                else:
                    volume = 0
                data_dict['volume'] = data_dict['volume'] + volume
            all_day.append(data_dict)
        return self.send_message(True, 0, 'success', all_day)


class CountProductTopSellHandler(BaseHandler):
    async def post(self, *args, **kwargs):
        user_id = self.verify_arg_legal(self.get_body_argument('userid'), '商家id')
        the_type = self.verify_arg_num(self.get_body_argument('type'), '类型', is_num=True)
        cur, conn = return_sqlserver_connect()
        search_item_sql = "select TmID,Name from Product where User_ID='{}'".format(user_id)
        print('search_item_sql', search_item_sql, the_type)
        if not cur:
            return self.send_message(True, 0, '没有数据', None)
        try:
            cur.execute(search_item_sql)
            the_results = cur.fetchall()
            conn.commit()
        except Exception as e:
            return self.send_message(True, 0, '没有数据', None)
        # 处理时间
        all_day = []
        for i in range(the_type):
            data_dict = {}
            the_day = (datetime.datetime.now() - datetime.timedelta(hours=i * 24)).date()
            this_day = str((datetime.datetime.now() - datetime.timedelta(hours=i * 24)).date()).replace('-', '_')
            # data_dict 每天的数据统计
            data_dict['day'] = str(the_day)
            data_dict['volume'] = 0
            for item in the_results:
                the_data = []
                this_day_collection = eval('self.db.products_{}'.format(this_day))
                async for doc in this_day_collection.find({"itemid": str(item[0])}):
                    the_data.append(doc)
                if the_data:
                    the_num = int(the_data[-1]['volume']) - int(the_data[0]['volume'])
                    volume = the_num if the_num >= 0 else 0
                else:
                    volume = 0
                data_dict['volume'] = data_dict['volume'] + volume
            all_day.append(data_dict)
        return self.send_message(True, 0, 'success', all_day)


if __name__ == '__main__':
    pass
