# 自定义存储方案
import cmspider
from cmspider import exception
from cmspider import config
from cmspider import UrlManager
from pymongo import errors
import json


class Store:
    conf = config
    count = 0

    # 存储列表
    def store_list(self, data):
        try:
            data = json.loads(data)

            # list.do
            # total_page = data['data']['totalPages']
            # conf['basic']['total_page'] = total_page
            # util.view_bar(count, total_page)
            # count += 1
            # for item in data['data']['content']:
            #     html_url = "http://www.neeq.com.cn" + item['htmlUrl']
            #     title = item['title']
            #     t = item['publishDate']
            #     timestamp = util.get_timestamp(t, f="%Y-%m-%d %H:%M:%S.0")
            #     url_manager.put_url(html_url, title, timestamp)

            # infoResult.do
            total_page = data['listInfo']['totalPages']
            self.conf['basic']['total_page'] = total_page
            for item in data['listInfo']['content']:
                file_url = "http://www.neeq.com.cn" + item['destFilePath']
                title = item['disclosureTitle']
                timestamp = item['upDate']['time']
                # 是否更新数据
                if not self.conf['basic']['fetch_all']:
                    if timestamp <= UrlManager().get_last_url("file")['timestamp']:
                        raise exception.ListFinishedException
                try:
                    UrlManager().put_url(file_url, title, timestamp, "file")
                except errors.DuplicateKeyError as dk:
                    pass
                    # TODO 改为这里验证，抛出完成异常
            cmspider.Util.view_bar(self.count, total_page)
            self.count += 1

        except Exception as e:
            raise e

    # 存储文章
    def store_article(self, dom):
        c = self.conf
        print(dom.h3.text)
        return True

    # 存储文件
    def store_file(self, data):
        pass
