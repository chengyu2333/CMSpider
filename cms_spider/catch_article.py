from cms_spider import config
from cms_spider import catch
from cms_spider import my_store
from cms_spider import filter
from cms_spider import url_manager
from pymongo import errors
conf = config.config
DUPLICATE_COUNT = 0

# 抓取单个文章
def catch_article(url):
    try:
        if "article" in conf['rule_html']:
            html = catch.catch_html(url)
            html = filter.dom_filter(html, conf['rule_html']['article']['css'], conf['rule_html']['article']['my_filter'])
            if html:
                print(url, " ok")
                url_manager.set_url(url, 2)
                my_store.store_article(html[0])
            else:
                url_manager.set_url(url, -1)
        elif "article" in conf['rule_api']:
            # TODO 从api获取文章
            pass
        else:
            raise Exception("没有配置文章抓取规则")
    except errors.DuplicateKeyError as e:
        global DUPLICATE_COUNT
        DUPLICATE_COUNT += 1
        print("重复文章", url)

# 递归爬取文章
def catch_article_recursive(url):
    try:
        if "article" in conf['rule_html']:
            print(url)
            html = catch.catch_html(url)
            if not html:
                return
            res = filter.dom_filter(html, conf['rule_html']['article']['css'], conf['rule_html']['article']['my_filter'])
            if res:
                url_manager.set_url(url, 2)
                my_store.store_article(res[0])
            else:
                url_manager.set_url(url, -1)
            # TODO 递归终止条件
            page = filter.dom_filter(html, conf['rule_html']['article']['page']['next_page']['css'])
            if page:
                new_url = filter.completion_url(page[0]['href'], url)
                catch_article_recursive(new_url)
            else:
                print("递归爬取完成")
        else:
            raise Exception("没有配置文章抓取规则")
    except errors.DuplicateKeyError as e:
        global DUPLICATE_COUNT
        DUPLICATE_COUNT += 1
        print("重复文章", url)
