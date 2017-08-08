# 自定义存储方案
from cms_spider import database
from cms_spider import config
from cms_spider import urls
from cms_spider import filter
import json

conf = config.config

# 存储列表
def store_list(data):
    try:
        data = json.loads(data)
        # infoResult.do
        # content = data['listInfo']['content']
        # last_page = data['listInfo']['lastPage']
        total_page = data['data']['totalPages']
        for item in data['data']['content']:
            html_url = "http://www.neeq.com.cn" + item['htmlUrl']
            title = item['title']
            re = urls.put_url(html_url, title)
            print(re)

        # total_element = data['listInfo']['totalElements']
        # print('last_page', last_page)
        # print('total_page', total_page)
        # # 动态修改总页数
        conf['basic']['total_page'] = total_page
        # print('total_ele',total_element)
        # print("content_len:",len(content))
        # print(data)
        # for item in content:
        #     print(item)
        #     database.DB().put_data(item, conf['db']['table_list'])

    except Exception as e:
        raise e


# 存储文章
def store_article(dom):
    print(dom.h3.text)
    return True


# 存储文件
def store_file(data):
    pass