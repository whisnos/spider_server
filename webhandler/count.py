import datetime

from webhandler.basehandler import BaseHandler
import pymssql

conn = pymssql.connect(host='192.168.32.24', port='1433', user='sa', password='shanpengfei@no1', database='TaoKe')
cur = conn.cursor()

class CountProductSellHandler(BaseHandler):
    async def post(self, *args, **kwargs):

        items = self.verify_arg_legal(self.get_body_argument('items'), '商品id')
        now = datetime.datetime.now()
        # now_prv = datetime.datetime.now() - datetime.timedelta(hours=2)
        now_prv = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,microseconds=now.microsecond)
        # day = now.day
        day = str(now.date()).replace('-', '_')
        item_list = items.split(',')
        collection = eval('self.db.products_{}'.format(day))
        # collection = eval('self.db.product_{}'.format(21))
        result = []
        for item in item_list:
            data_dict = {}
            the_data=[]
            async for doc in collection.find({"itemid": str(item), "createTime": {"$gte": now_prv, "$lte": now}}):
                # doc.pop('_id', '404')
                # doc.pop('createTime', '404')
                the_data.append(doc)
            if the_data:
                the_num = int(the_data[-1]['volume'])-int(the_data[0]['volume'])
                volume = the_num if the_num >= 0 else 0
                data_dict['itemid']=item
                data_dict['volume'] = volume
                result.append(data_dict)
            else:
                data_dict['itemid'] = item
                data_dict['volume'] = 0
                result.append(data_dict)
        return self.send_message(True, 0, 'success', result)


class CountUserProductSellHandler(BaseHandler):
    async def post(self, *args, **kwargs):
        print(123)
        user_id = self.verify_arg_legal(self.get_body_argument('userid'), '商家id')
        the_type = self.verify_arg_num(self.get_body_argument('type'), '类型',is_num=True)
        search_item_sql = "select TmID,Name from Product where User_ID='{}'".format(user_id)
        print('search_item_sql', search_item_sql,the_type)
        try:
            cur.execute(search_item_sql)
            the_results = cur.fetchall()
            conn.commit()
        except Exception as e:
            print(123,e)
        print('the_results',the_results)
        for item in the_results:
            print('itemid',item[0])
        now = datetime.datetime.now()
        now_prv = datetime.datetime.now() - datetime.timedelta(hours=the_type*24)
        print('now_prv',now_prv)
        prv_day = now_prv.day
        prv_day = str(prv_day).replace('-', '_')
        prv_day_collection = eval('self.db.products_{}'.format(prv_day))
        async for doc in prv_day_collection.find({"itemid": str(item), "createTime": {"$gte": now_prv, "$lte": now}}):
            # doc.pop('_id', '404')
            # doc.pop('createTime', '404')
            the_data.append(doc)
        if the_data:
            the_num = int(the_data[-1]['volume'])-int(the_data[0]['volume'])
            volume = the_num if the_num >= 0 else 0
            data_dict['itemid']=item
            data_dict['volume'] = volume
            result.append(data_dict)
        # # day = now.day
        # day = str(now.date()).replace('-', '_')
        # item_list = items.split(',')
        # collection = eval('self.db.products_{}'.format(day))
        # # collection = eval('self.db.product_{}'.format(21))
        # result = []
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
        return self.send_message(True, 0, 'success', the_results)


if __name__ == '__main__':
    pass
