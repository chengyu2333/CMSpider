from cms_spider import my_filter

# 说明：
# 1.使用##page##来标记页码
# 2.匹配规则css、filter将会依次应用在源数据中
config = {
    # 数据库配置
    "db": {
        "type": "mongodb",
        "host": "127.0.0.1",
        "port": 12345,
        "db_name": "neeq",
        "user": "",
        "password": "",
        # 表名
        "table_column": "column",
        "table_list": "url",
        "table_article": "article",
        "table_file": "file",
    },
    # 基础配置
    "basic": {
        "timeout": 5,  # 连接超时时间
        "max_thread": 10,  # 最大线程
        "entry_url": "http://www.neeq.com.cn",
        "start_page": 0,  # 起始页
        "max_page": 999,  # 最多爬取的页数
        "total_page": 10,  # 总页数可动态修改
        "start_date": "",  # 开始日期
        "end_date": "",  # 结束日期
        "header": {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"},
    },
    # api抓取规则
    "rule_api": {
        # 列表api规则
        "list": {
            "method": "post",
            # "url": "http://www.neeq.com.cn/disclosureInfoController/infoResult.do",
            "url": "http://www.neeq.com.cn/info/list.do",
            # "url": "http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?id=128367438&s=10&cp=##page##&priority=1",
            # POST数据
            "args": {
                # list.do
                "page": "##page##",
                "pageSize": "10",
                "keywords": "",
                "publishDate": "",
                "nodeId": "93",
                # infoResult.do
                # "disclosureType": "6",
                # "page": "##page##",
                # "isNewThree": "1",
                # "startTime": "2016-08-07",
                # "endTime": "2017-08-07",
            },
            "my_filter": my_filter.rule_api_list,  # 自定义结果过滤器
        },
        # 文章api规则
        "article": {
        },
    },
    # 网页抓取规则
    "rule_html": {
        # 板块抓取规则
        "column": {
            "css": "",
            "my_filter": my_filter.rule_html_column
        },
        # 列表抓取规则
        "list": {
            "url": "http://forex.hexun.com/market/index-##page##.html",
            "css": ".mainboxcontent ul li",
            "my_filter": my_filter.rule_html_list,
            "page": {
                # 递归时配置
                "next_page": {
                    "css": "",
                    "my_filter": my_filter.rule_html_list_page
                },
                "page_list": {
                }
            }
        },
        # 文章抓取规则
        "article": {
            # http://www.neeq.com.cn/notice/20000477.html
            "source": "",  # url来源：空，数据库，不为空，递归
            "css": ".newstext",  # 文章主体dom
            "my_filter": my_filter.rule_html_article,
            "page": {
                # 递归时配置
                "next_page": {
                    "css": ".next a",
                    "my_filter": my_filter.rule_html_article_page
                }
            }
        },
        # 文件抓取规则
        "file": {
            "function_path": "",
            "page": {
                # 递归时配置
                "next_page": {
                    "css": "",
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
