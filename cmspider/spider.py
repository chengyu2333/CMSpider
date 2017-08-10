import json
from cmspider import UrlManager
from cmspider import Fetch
from cmspider import fetch_list
from cmspider import fetch_article
from cmspider import config

import os

conf = config


class Spider:
    def __init__(self, conf=None):
        if conf:
            try:
                self.conf = json.loads(conf)
            except Exception as e:
                raise

    @staticmethod
    def run_all(self):
        self.fetch_url()
        self.fetch_article()
        self.fetch_file()

    @staticmethod
    def fetch_url():
        print("开始抓取url列表")
        fetch_list.fetch_list_multi()

    # 爬取文章
    @staticmethod
    def fetch_article():
        print("开始抓取文章")
        source = conf['article']['html']['source']
        if source:
            fetch_article.fetch_article_recursive(conf['article']['html']['source'])
        else:
            while True:
                url = UrlManager().get_url(10, "html")
                if not url:
                    break
                for u in url:
                    fetch_article.fetch_article(u['_id'])
        print("文章抓取完成")

    # 爬取文件
    @staticmethod
    def fetch_file():
        print("开始下载文件")
        while True:
            url = UrlManager().get_url(10, "file")
            if not url:
                break
            for u in url:
                path = conf['file']['basic_path'] + conf['file']['hash_path'](u["_id"])
                if not os.path.exists(path):
                    os.makedirs(path)
                filename = u["_id"].split(".")[-1].split("?")[0]
                full_path = path + u['title'] + "." + conf['file']['hash_filename'](filename)
                print("\r"+full_path, end="")
                Fetch().fetch_file(u['_id'], full_path)
        print("文件下载完成")

    @staticmethod
    def recover_status():
        UrlManager().set_all_status()
        pass

