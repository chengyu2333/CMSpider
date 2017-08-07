# 自定义存储方案
from cms_spider import database
from cms_spider import config
import json

conf = config.config


def store_url(data):
    print(data)
    try:
        data = json.loads(data)
        content = data['listInfo']['content']
        last_page = data['listInfo']['lastPage']
        total_page = data['listInfo']['totalPages']
        total_element = data['listInfo']['totalElements']
        print('last_page', last_page)
        print('total_page', total_page)
        # 动态修改总页数
        conf['basic']['total_page'] = total_page
        print('total_ele',total_element)
        print("content_len:",len(content))
        print(data)
        for item in content:
            # print(item)
            database.DB().put_data(item, conf['db']['table_list'])
    except Exception as e:
        print(e)


def store_article(data):
    print(data.title)


def store_element(data):
    pass