from webhandler import basehandler
import tornado.web

from webhandler.count import CountProductSellHandler, CountUserProductSellHandler, CountProductTopSellHandler, \
    CountProductHourTopSellHandler, CountUserTodayTopSellHandler, ProcessDouYinGrowHandler, ProcessVideoTopHandler, \
    ProcessTurnLinkHandler, ProcessProductInfoHandler
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
        # (r"/count/productsellcount", CountProductSellHandler),                     # 计算20个销量
        (r"/count/usersell", CountUserProductSellHandler),                           # 根据商家id计算商品销量
        # (r"/count/topsell", CountProductTopSellHandler),                           # 根据销量计算全天榜单100
        # (r"/count/hoursell", CountProductHourTopSellHandler),                      # 根据销量计算2个小时榜单100
        # (r"/count/todaysell", CountUserTodayTopSellHandler),                       # 根据商户id计算当天销量聚合总数
        (r"/process/douyingrow", ProcessDouYinGrowHandler),                          # 动态查看抖音主播粉丝增量
        (r"/process/videotop", ProcessVideoTopHandler),                              # 处理 有道
        (r"/process/turnlink", ProcessTurnLinkHandler),                              # 直播榜单数据
        # (r"/process/turntotal", ProcessTurnTotalHandler),                          # 返回店铺销量
        (r"/process/productinfo", ProcessProductInfoHandler),                        # 返回产品信息
        # (r"/count/catesell", CountProductCateTopSellHandler),                      # 根据类目计算榜单100
        ],
        # cookie_secret = 'cb56YAgMjpevlWBNqgrv5g==',
        # login_url = '/',
        # xheader= True,
        # debug = True,
        # autoreload = True,
        # serve_traceback= True
    )