# 自定义存储方案
from cmspider import Util
from cmspider import exception
from cmspider import config
from cmspider import UrlManager
from pymongo import errors
import json


class Store:
    url_manager = UrlManager()
    count = 0

    # 存储列表
    def store_list(self, data):
        try:
            data = json.loads(data)

            # list.do
            total_page = data['data']['totalPages']
            config['basic']['total_page'] = total_page
            Util.view_bar(self.count, total_page)
            self.count += 1
            for item in data['data']['content']:
                html_url = "http://www.neeq.com.cn" + item['htmlUrl']
                title = item['title']
                t = item['publishDate']
                timestamp = Util.get_timestamp(t, f="%Y-%m-%d %H:%M:%S.0")
                self.url_manager.put_url(html_url, title, timestamp, "html")

            # infoResult.do
            # total_page = data['listInfo']['totalPages']
            # config['basic']['total_page'] = total_page
            # for item in data['listInfo']['content']:
            #     file_url = "http://www.neeq.com.cn" + item['destFilePath']
            #     title = item['disclosureTitle']
            #     timestamp = item['upDate']['time']
            #     # 是否更新数据
            #     if not config['basic']['fetch_all']:
            #         if timestamp <= self.url_manager.get_last_url("file")['timestamp']:
            #             raise exception.ListFinishedException
            #     try:
            #         UrlManager().put_url(file_url, title, timestamp, "file")
            #     except errors.DuplicateKeyError as dk:
            #         pass
            #         # TODO 改为这里验证，抛出完成异常

            Util.view_bar(self.count, total_page)  #进度条
            self.count += 1

        except Exception as e:
            raise e

    # 存储文章
    def store_article(self, res, url):
       pass

    # 存储文件
    # def store_file(self, data):
    #     pass
