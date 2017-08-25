import json
from cmspider.util import Util
from cmspider.url_manager import UrlManager
from cmspider.fetch_file import FetchFile
from cmspider.fetch_list import FetchList
from cmspider.fetch_article import FetchArticle
from cmspider.config import config


class Spider:
    farticle = FetchArticle()
    flist = FetchList()
    ffile = FetchFile()
    conf = config

    def __init__(self, conf=None):
        if conf:
            try:
                self.conf.update(json.loads(conf))
            except Exception as e:
                raise

    @staticmethod
    def run_all(self):
        self.fetch_url()
        self.fetch_article()
        self.fetch_file()

    def fetch_url(self):
        print("开始抓取url列表")
        self.flist.fetch_list_multi()
        Util.COUNT_SUCCESS = 0
        Util.COUNT_DUPLICATE = 0

    # 爬取文章
    def fetch_article(self):
        print("开始抓取文章")
        self.farticle.fetch_article_multi()
        Util.COUNT_SUCCESS = 0
        Util.COUNT_DUPLICATE = 0

    # 爬取文件
    def fetch_file(self):
        print("开始下载文件")
        self.ffile.fetch_file_multi()
        Util.COUNT_SUCCESS = 0
        Util.COUNT_DUPLICATE = 0
        print("文件下载完成")

    @staticmethod
    def recover_status():
        UrlManager().set_all_status()
        pass

