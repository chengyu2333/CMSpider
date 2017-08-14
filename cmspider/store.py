# 自定义存储方案
from cmspider import Util
from cmspider import exception
from cmspider import config
from cmspider import UrlManager
from pymongo import errors
from cmspider import DB
import json


class Store:
    url_manager = UrlManager()
    db = DB()
    count = 0

    # 存储文章列表
    def store_article_list(self, data):
        pass

    # 存储文件列表
    def store_file_list(self, data):
        pass

    # 存储文章
    def store_article(self, res, url):
        pass
