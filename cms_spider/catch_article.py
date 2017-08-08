from cms_spider import config
from cms_spider import catch
from cms_spider import my_store
from cms_spider import filter
from cms_spider import urls
conf = config.config


# 抓取单个文章
def catch_article(url):
    if "article" in conf['rule_html']:
        html = catch.catch_html(url)
        html = filter.dom_filter(html, conf['rule_html']['article']['css'], conf['rule_html']['article']['my_filter'])
        if html:
            print(url, 2)
            urls.set_url(url, 2)
            my_store.store_article(html[0])
        else:
            urls.set_url(url, -1)
    else:
        raise Exception("没有配置文章抓取规则")


# 递归爬取文章
def catch_article_recursive(url):
    if "article" in conf['rule_html']:
        print(url)
        html = catch.catch_html(url)
        if not html:
            return
        res = filter.dom_filter(html, conf['rule_html']['article']['css'], conf['rule_html']['article']['my_filter'])
        if res:
            urls.set_url(url, 2)
            my_store.store_article(res[0])
        else:
            urls.set_url(url, -1)
        # TODO 递归终止条件
        page = filter.dom_filter(html, conf['rule_html']['article']['page']['next_page']['css'])
        if page:
            new_url = filter.completion_url(page[0]['href'], url)
            catch_article_recursive(new_url)
        else:
            print("递归爬取完成")
    else:
        raise Exception("没有配置文章抓取规则")

