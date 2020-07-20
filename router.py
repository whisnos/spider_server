﻿from webhandler import basehandler
import tornado.web

from webhandler.count import CountProductSellHandler
from webhandler.item import ItemCommentDetailHandler, ItemCommentTagListDetailHandler
from webhandler.test import TestHandler


class MainHandler(basehandler.BaseHandler):
    def get(self):
        # print(self.request.body, self.request.query)
        self.write("Hello, get!")

    def post(self):
        # print(self.request.body, self.request.query)
        self.write("Hello, post!")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/test", TestHandler),                                                     # 测试api
        (r"/item/commenttaglist", ItemCommentTagListDetailHandler),                  # 获取商品评论标签
        (r"/item/commentdetail", ItemCommentDetailHandler),                          # 获取商品评论详情
        (r"/count/productsellcount", CountProductSellHandler),                       # 计算商品销量
        ],
        # cookie_secret = 'cb56YAgMjpevlWBNqgrv5g==',
        # login_url = '/',
        # xheader= True,
        # debug = True,
        # autoreload = True,
        # serve_traceback= True
    )