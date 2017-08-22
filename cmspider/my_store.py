from cmspider.store import Store
from cmspider.config import config
from cmspider.util import Util
from cmspider import exception
from pymongo import errors
import json


class MyStore(Store):
    def __init__(self):
        pass
        # 存储列表

    def store_file_list(self, data):
        data = json.loads(data)
        # infoResult.do
        total_page = data['listInfo']['totalPages']
        config['basic']['total_page'] = total_page
        for item in data['listInfo']['content']:
            file_url = "http://www.neeq.com.cn" + item['destFilePath']
            title = item['disclosureTitle']
            timestamp = item['upDate']['time']
            # 到达最新数据
            # if config['basic']['max_replicate']:
            #     if timestamp <= self.url_manager.get_last_url("file")['timestamp']:
            #         raise exception.ListFinishedException
            try:
                self.url_manager.put_url(file_url, title, timestamp, "file")
                # 如果抓取成功则把重复数量设置为0
                Util.COUNT_DUPLICATE = 0
                Util.COUNT_SUCCESS += 1
            except errors.DuplicateKeyError as dk:
                # 连续重复数量+1
                Util.COUNT_DUPLICATE += 1
                if config['list']['max_replicate']:
                    if Util.COUNT_DUPLICATE > config['list']['max_replicate']:
                        Util.COUNT_DUPLICATE = 0
                        raise exception.ExceedMaxDuplicate
                        # 超过最大连续重复次数，视为已抓取完最新数据

        Util.view_bar(Util.COUNT_PROCESSED, total_page)
        Util.COUNT_PROCESSED += 1

    def store_article_list(self, data):
        data = json.loads(data)
        # list.do
        total_page = data['data']['totalPages']
        config['basic']['total_page'] = total_page
        for item in data['data']['content']:
            html_url = "http://www.neeq.com.cn" + item['htmlUrl']
            title = item['title']
            t = item['publishDate']
            timestamp = Util.get_timestamp(t, f="%Y-%m-%d %H:%M:%S.0")
            try:
                self.url_manager.put_url(html_url, title, timestamp, "html")
                Util.COUNT_DUPLICATE = 0
                Util.COUNT_SUCCESS += 1
            except errors.DuplicateKeyError as dk:
                Util.COUNT_DUPLICATE += 1
                if config['list']['max_replicate']:
                    if Util.COUNT_DUPLICATE > config['list']['max_replicate']:
                        Util.COUNT_DUPLICATE = 0
                        raise exception.ExceedMaxDuplicate

        Util.view_bar(Util.COUNT_PROCESSED, total_page)
        Util.COUNT_PROCESSED += 1

    def store_article(self, res, url):
        if res:
            res['_id'] = url
            print(url, "\t", res['title'])
            try:
                self.db.put_article(res)
                Util.COUNT_DUPLICATE = 0
                Util.COUNT_SUCCESS += 1
            except errors.DuplicateKeyError as dk:
                Util.COUNT_DUPLICATE += 1
                if config['article']['max_replicate']:
                    if Util.COUNT_DUPLICATE > config['article']['max_replicate']:
                        Util.COUNT_DUPLICATE = 0
                        raise exception.ExceedMaxDuplicate
            self.url_manager.set_url_status(url, 2)
        else:
            self.url_manager.set_url_status(url, -1)
