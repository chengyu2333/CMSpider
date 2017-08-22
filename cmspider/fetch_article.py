from cmspider.config import config
from cmspider.fetch import Fetch
from cmspider.store import Store
from cmspider.filter import Filter
from cmspider.util import Util
from cmspider.url_manager import UrlManager
from cmspider.exception import ExceedMaxDuplicate
from pymongo import errors


class FetchArticle(Fetch):
    url_manager = UrlManager()
    store = Store()
    duplicate_count = 0

    # 抓取单个文章
    def fetch_article(self, url):
        try:
            if "html" in config['article']:
                html = self.fetch_html(url)
                Filter(html, config['article']['html']).store("article", url)
            elif "api" in config['article']:
                # TODO 从api获取文章
                pass
            else:
                raise Exception("没有配置文章抓取规则")
        except errors.DuplicateKeyError as e:
            self.duplicate_count += 1
            print("重复文章", url)

    # 递归爬取文章
    def fetch_article_recursive(self, url):
        try:
            if "html" in config['article']:
                html = self.fetch_html(url)
                if not html:
                    return
                Filter(html, config['article']['html']).store("article", url)

                # TODO 递归终止条件
                page = Filter().dom_filter(html, config['article']['html']['recursive']['next_page']['css'])
                if page:
                    new_url = Filter.completion_url(page[0]['href'], url)
                    self.fetch_article_recursive(new_url)
                else:
                    print("递归爬取完成")
            else:
                raise Exception("没有配置文章抓取规则")
        except ExceedMaxDuplicate:
            Util.COUNT_DUPLICATE = 0
            Util.COUNT_SUCCESS = 0
            print("递归更新完成,数量：", Util.COUNT_SUCCESS)

    # 爬取文章
    def fetch_article_multi(self, once=False):
        source = config['article']['html']['source']
        if source:
            self.fetch_article_recursive(config['article']['html']['source'])
        else:
            while True:
                url = self.url_manager.get_url(file_type="html")
                if not url:
                    break
                for u in url:
                    self.fetch_article(u['_id'])
                if once:
                    break
            print("\n全部文章抓取完成,数量：", Util.COUNT_SUCCESS)
        Util.COUNT_SUCCESS = 0
