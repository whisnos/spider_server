import json
import re

from tool.function import Return_headers
from webhandler.basehandler import BaseHandler
from aiohttp_requests import requests


class ItemCommentTagListDetailHandler(BaseHandler):
    async def post(self, *args, **kwargs):
        msg = '操作成功'
        itemid = self.verify_arg_num(self.get_body_argument('itemid'), '商品id', is_num=True)
        base_url = 'https://rate.tmall.com/listTagClouds.htm?itemId={}&isAll=true'
        headers = Return_headers()
        r = await requests.get(base_url.format(itemid), headers=headers, timeout=5)
        html = await r.text()
        tag_Obj = re.search(r'\((.*)\)', html, re.M | re.I)
        try:
            pin_num = tag_Obj.group(1)
            data_dict = json.loads(pin_num)
            return self.send_message(True, 0, msg, data_dict)
        except Exception as e:
            data_dict = {}
            msg = '获取失败'
        return self.send_message(False, 400, msg, data_dict)


class ItemCommentDetailHandler(BaseHandler):
    async def post(self, *args, **kwargs):
        msg = '操作成功'
        itemid = self.verify_arg_num(self.get_body_argument('itemid'), '商品id', is_num=True)
        page = self.verify_arg_num(self.get_body_argument('page', '1'), '页数', is_num=True)
        tagid = self.verify_arg_legal(self.get_body_argument('tagid', ''), '页数')
        base_url = 'https://rate.tmall.com/list_detail_rate.htm?itemId={}&sellerId=708498884&order=3&currentPage={}&append=0&content=1&tagId={}&callback=jsonp606'
        headers = Return_headers()
        r = await requests.get(base_url.format(itemid, page, tagid), headers=headers, timeout=5)
        html = await r.text()
        comment_Obj = re.search(r'jsonp606\((.*)\)', html, re.M | re.I)
        try:
            pin_num = comment_Obj.group(1)
            data_dict = json.loads(pin_num)
            return self.send_message(True, 0, msg, data_dict)
        except Exception as e:
            data_dict = {}
            msg = '获取失败'
        return self.send_message(False, 400, msg, data_dict)


if __name__ == '__main__':
    pass
