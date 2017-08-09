import json
from cms_spider import catch
from cms_spider import catch_list
from cms_spider import catch_article
from cms_spider import config
from cms_spider import url_manager
import os

conf = config.config


class Spider:
    def __init__(self, config=None):
        if config:
            try:
                self.conf = json.loads(config)
            except Exception as e:
                raise

    def run(self):
        self.catch_url()
        self.catch_article()
        self.catch_file()


    def catch_url(self):
        catch_list.catch_list_multi()

    # 爬取文章
    def catch_article(self):
        source = conf['rule_html']['article']['source']
        if source:
            catch_article.catch_article_recursive(conf['rule_html']['article']['source'])
        else:
            while True:
                url = url_manager.get_url(10, "html")
                if not url:
                    break
                for u in url:
                    catch_article.catch_article(u['_id'])

    def catch_file(self):
        while True:
            url = url_manager.get_url(10, "file")
            if not url:
                break
            for u in url:
                path = conf['rule_html']['file']['basic_path'] + conf['rule_html']['file']['hash_path'](u["_id"])
                if not os.path.exists(path):
                    os.makedirs(path)
                filename = u["_id"].split(".")[-1].split("?")[0]
                full_path = path + u['title'] + "." + conf['rule_html']['file']['hash_filename'](filename)
                print(full_path)
                catch.catch_file(u['_id'], full_path)

    def recover_status(self):
        url_manager.recover_status()
        pass

