# 自定义存储方案
from cms_spider import util
from cms_spider import exception
from cms_spider import config
from cms_spider import url_manager
from pymongo import errors
import json

conf = config.config
count = 0

# 存储列表
def store_list(data):
    global count
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
        conf['basic']['total_page'] = total_page
        for item in data['listInfo']['content']:
            file_url = "http://www.neeq.com.cn" + item['destFilePath']
            title = item['disclosureTitle']
            timestamp = item['upDate']['time']
            # 是否更新数据
            if not conf['basic']['catch_all']:
                if timestamp <= url_manager.get_last_url("file")['timestamp']:
                    raise exception.ListFinishedException
            try:
                url_manager.put_url(file_url, title, timestamp, "file")
            except errors.DuplicateKeyError as dk:
                pass
                # TODO 改为这里验证，抛出完成异常
        util.view_bar(count, total_page)
        count += 1

    except Exception as e:
        raise e


# 存储文章
def store_article(dom):
    print(dom.h3.text)
    return True


# 存储文件
def store_file(data):
    pass