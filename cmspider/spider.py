import json
from cmspider import UrlManager
from cmspider import FetchFile
from cmspider import FetchList
from cmspider import FetchArticle
from cmspider import config
from pymongo import errors


class Spider:
    farticle = FetchArticle()
    flist = FetchList()
    ffile = FetchFile()
    url_manager = UrlManager()

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

    def fetch_url(self):
        print("开始抓取url列表")
        try:
            self.flist.fetch_list_multi()
        except Exception as e:
            print(str(e))

    # 爬取文章
    def fetch_article(self, once=False):
        print("开始抓取文章")
        source = config['article']['html']['source']
        if source:
            self.farticle.fetch_article_recursive(config['article']['html']['source'])
        else:
            while True:
                url = self.url_manager.get_url(config['article']['html']['max_num'], "html")
                if not url:
                    break
                for u in url:
                    self.farticle.fetch_article(u['_id'])
                if once:
                    break
        print("\n文章抓取完成")

    # 爬取文件
    def fetch_file(self):
        print("开始下载文件")
        while True:
            urls = self.url_manager.get_url(config['file']['max_num'], "file")
            if not urls:
                break
            for url_obj in urls:
                self.ffile.fetch_file(url_obj)

        print("文件下载完成")

    @staticmethod
    def recover_status():
        UrlManager().set_all_status()
        pass

