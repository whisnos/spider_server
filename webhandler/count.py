import datetime

from webhandler.basehandler import BaseHandler


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


if __name__ == '__main__':
    pass
