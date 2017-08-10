from cmspider import config
from cmspider import fetch
from cmspider import my_store
from cmspider import my_filter
from cmspider import url_manager
from pymongo import errors
conf = config
DUPLICATE_COUNT = 0


# 抓取单个文章
def fetch_article(url):
    try:
        if "html" in conf['article']:
            html = fetch.fetch_html(url)
            html = my_filter.dom_filter(html, conf['article']['html']['css'], conf['article']['html']['my_filter'])
            if html:
                print(url, " ok")
                url_manager.set_url_status(url, 2)
                my_store.store_article(html[0])
            else:
                url_manager.set_url_status(url, -1)
        elif "api" in conf['article']:
            # TODO 从api获取文章
            pass
        else:
            raise Exception("没有配置文章抓取规则")
    except errors.DuplicateKeyError as e:
        global DUPLICATE_COUNT
        DUPLICATE_COUNT += 1
        print("重复文章", url)


# 递归爬取文章
def fetch_article_recursive(url):
    try:
        if "html" in conf['article']:
            print(url)
            html = fetch.fetch_html(url)
            if not html:
                return
            res = my_filter.dom_filter(html, conf['article']['html']['css'], conf['article']['html']['my_filter'])
            if res:
                url_manager.set_url_status(url, 2)
                my_store.store_article(res[0])
            else:
                url_manager.set_url_status(url, -1)
            # TODO 递归终止条件
            page = my_filter.dom_filter(html, conf['article']['html']['page']['next_page']['css'])
            if page:
                new_url = my_filter.completion_url(page[0]['href'], url)
                fetch_article_recursive(new_url)
            else:
                print("递归爬取完成")
        else:
            raise Exception("没有配置文章抓取规则")
    except errors.DuplicateKeyError as e:
        global DUPLICATE_COUNT
        DUPLICATE_COUNT += 1
        print("重复文章", url)
