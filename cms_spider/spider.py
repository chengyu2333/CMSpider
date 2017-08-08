import json
from cms_spider import catch
from cms_spider import catch_list
from cms_spider import catch_article
from cms_spider import database
from cms_spider import config
from cms_spider import urls

conf = config.config


class Spider:
    def __init__(self, config=None):
        if config:
            try:
                self.config = json.loads(config)
            except Exception as e:
                raise

    def run(self):
        print("run", self.config)


    def catch_url(self):
        catch_list.catch_list_multi()

    # 爬取文章
    def catch_article(self):
        source = conf['rule_html']['article']['source']
        if source:
            catch_article.catch_article_recursive(conf['rule_html']['article']['source'])
        else:
            while True:
                url = urls.get_url(10)
                if not url:
                    break
                for u in url:
                    catch_article.catch_article(u['_id'])

    def catch_file(self):
        while True:
            url = urls.get_url(10)
            if not url:
                break
            for u in url:
                catch.catch_file(['_id'], path)

    def recover_status(self):
        database.DB().recover_status()
        pass

