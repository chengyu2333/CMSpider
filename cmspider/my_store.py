from cmspider import Store
from cmspider import config
from cmspider import Util
from cmspider import exception
from pymongo import errors
import json


class MyStore(Store):
    # count = 0

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
            # 是否更新数据
            if not config['basic']['fetch_all']:
                if timestamp <= self.url_manager.get_last_url("file")['timestamp']:
                    raise exception.ListFinishedException
            try:
                self.url_manager.put_url(file_url, title, timestamp, "file")
            except errors.DuplicateKeyError as dk:
                self.count += 1
                raise
                # TODO 抛出完成异常
        print(self.count,"  ",total_page)
        Util.view_bar(self.count, total_page)  # 进度条
        self.count += 1

    def store_article_list(self, data):
        # self.count += 1
        try:
            data = json.loads(data)
            # list.do
            total_page = data['data']['totalPages']
            config['basic']['total_page'] = total_page
            for item in data['data']['content']:
                html_url = "http://www.neeq.com.cn" + item['htmlUrl']
                title = item['title']
                t = item['publishDate']
                timestamp = Util.get_timestamp(t, f="%Y-%m-%d %H:%M:%S.0")
                self.url_manager.put_url(html_url, title, timestamp, "html")

            # print(self.count, " ", total_page)
            Util.view_bar(self.count, total_page)  # 进度条
            self.count += 1

        except Exception as e:
            raise e
            # 存储文章

    def store_article(self, res, url):

        if res:
            res['_id'] = url
            print(res['title'])
            self.db.put_article(res)
            self.url_manager.set_url_status(url, 2)
        else:
            self.url_manager.set_url_status(url, -1)
