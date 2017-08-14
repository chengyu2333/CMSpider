from cmspider import config
from cmspider import Fetch
from cmspider import Store
from cmspider import Filter
from pymongo import errors
DUPLICATE_COUNT = 0


class FetchArticle(Fetch):
    store = Store()

    # 抓取单个文章
    def fetch_article(self, url):
        try:
            if "html" in config['article']:
                html = self.fetch_html(url)
                # html = Filter.dom_filter(html, config['article']['html']['css'], config['article']['html']['my_filter'])
                Filter(html, config['article']['html']).store("article", url)

            elif "api" in config['article']:
                # html = self.fetch_html(url)
                # Filter(html, config['article']['api']).store_article()
                # TODO 从api获取文章
                pass
            else:
                raise Exception("没有配置文章抓取规则")
        except errors.DuplicateKeyError as e:
            global DUPLICATE_COUNT
            DUPLICATE_COUNT += 1
            print("重复文章", url)

    # 递归爬取文章
    def fetch_article_recursive(self, url):
        try:
            if "html" in config['article']:
                print(url)
                html = self.fetch_html(url)
                if not html:
                    return
                # res = Filter.dom_filter(html, config['article']['html']['css'], config['article']['html']['my_filter'])
                Filter(html, config['article']['html']).store("article", url)

                # TODO 递归终止条件
                page = Filter.dom_filter(html, config['article']['html']['page']['next_page']['css'])
                if page:
                    new_url = Filter.completion_url(page[0]['href'], url)
                    self.fetch_article_recursive(new_url)
                else:
                    print("递归爬取完成")
            else:
                raise Exception("没有配置文章抓取规则")
        except errors.DuplicateKeyError as e:
            global DUPLICATE_COUNT
            DUPLICATE_COUNT += 1
            print("重复文章", url)celery
