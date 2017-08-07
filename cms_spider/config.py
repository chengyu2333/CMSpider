from cms_spider import my_filter
# 说明：
# 1.使用##page##来标记页码
# 2.匹配规则css、dom、filter将会依次应用在源数据中
config = {
    "db": {
        "type": "mongodb",
        "host": "127.0.0.1",
        "port": 12345,
        "db_name": "neeq",
        "user": "",
        "password": "",
        "table_column": "column",
        "table_list": "url",
        "table_element": "article"
    },
    "basic": {
        "timeout": 5,  # 连接超时时间
        "max_thread": 10,  # 最大线程
        "entry_url": "http://www.neeq.com.cn",
        "start_page": 0,  # 起始页
        "max_page": 999,  # 最多爬取的页数
        "total_page": 10,  # 建议动态获取
        "start_date": "",  # 开始日期
        "end_date": "",  # 结束日期
        "header": {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"},
    },
    # 通过api获取
    # "rule_api": {
    #     "list": {
    #         "method": "post",
    #         "url": "http://www.neeq.com.cn/disclosureInfoController/infoResult.do",
    #         # "url": "http://www.neeq.com.cn/info/list.do",
    #         # "url": "http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?id=128367438&s=10&cp=##page##&priority=1",
    #         # POST数据
    #         "args": {
    #             # "page": "##page##",
    #             # "pageSize": "10",
    #             # "keywords": "",
    #             # "publishDate": "",
    #             # "nodeId": "93",
    #
    #             "disclosureType": "6",
    #             "page": "##page##",
    #             "isNewThree": "1",
    #             "startTime": "2016-08-07",
    #             "endTime": "2017-08-07",
    #         },
    #         "my_filter": my_filter.rule_api_list  # 自定义结果过滤器
    #     },
    #     "article": {
    #     },
    # },
    # 通过网页抓取
    "rule_html": {
        "column": {
            "css": "",
            "regular": "(.*?)",
            "my_filter": my_filter.rule_html_column
        },
        "list": {
            "url": "http://forex.hexun.com/market/index-##page##.html",
            "css": "",
            "regular": "(.*?)",
            "my_filter": my_filter.rule_html_list,
            "page": {
                "next_page": {
                    "css": "",
                    "regular": "(.*?)",
                    "my_filter": my_filter.rule_html_list_page
                },
                "page_list": {
                }
            }
        },
        "article": {
            "css": "",
            "regular": "(.*?)",
            "my_filter": my_filter.rule_html_article,
            "content": {
                "title": {},
                "author": {},
                "time": {},
                "body": {}
            },
            "page": {
                "next_page": {
                    "css": "",
                    "regular": "(.*?)",
                    "my_filter": my_filter.rule_html_article_page
                }
            }
        },
        "file": {
            "suffix": "jpg",
            "function_path": "",
            "page": {
                "next_page": {
                    "css": "",
                    "regular": "(.*?)",
                    "my_filter": my_filter.rule_file_page
                }
            }
        }
    }
}


# 根据值查找键
def get_dict_key(d, value):
    for k, v in d.items():
        if v == value:
            return k
    return None
