from cmspider.config import config
conf = {
    # 数据库配置
    "db": {
        "type": "mongodb",
        "host": "q.213.name",
        "port": 27017,
        "db_name": "neeq",
        "user": "",
        "password": "",
        # 各表名
        "table_column": "column",
        "table_list": "url",
        "table_article": "article",
        "table_file": "file",
    },
    # 爬虫基础配置
    "basic": {
        "timeout": 5,  # 连接超时时间
        "max_thread": 10,  # 最大线程
        "header": {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) "
                                 "Chrome/59.0.3071.86 Safari/537.36",
                   "cookie": "",
                   },
        "entry_url": "http://www.neeq.com.cn",
        "start_page": 0,  # 起始页
        "max_page": 999,  # 最多爬取的页数
        "total_page": 2500,  # 总页数,建议动态修改

        # "fetch_all": True,  # 是否抓取全部，False为增量更新数据，第一次运行时选择True
    },
    # 板块（API）抓取规则
    "column": {
        "css": "",
        "my_filter": "MyFilter.rule_html_column"
    },
    # URL列表抓取规则
    "list": {
        "max_replicate": 100,  # 连续重复多少次则停止抓取url，0为不限 (重新抓取全部时则设置为0)
        # 通过api获取
        "api": {
            # "filetype": "file",  # html | file
            "method": "post",
            # "url": "http://www.neeq.com.cn/disclosureInfoController/infoResult.do",
            "url": "http://www.neeq.com.cn/info/list.do",
            # "url": "http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp?id=128367438&s=10"
            #        "&cp=##page##&priority=1",
            # POST数据
            "post_data": {
                # list.do 文章
                "page": "##page##",
                "pageSize": "10",
                "keywords": "",
                "publishDate": "",
                "nodeId": "93",
                # infoResult.do 文件
                # "disclosureType": "5",
                # "page": "##page##",
                # "isNewThree": "1",
                # "startTime": "2016-08-07",
                # "endTime": "2017-08-07",
            },
            "my_filter": "rule_api_list",
            "store": "store_article_list"
            # "store": "store_file_list"
        },
        # 通过html爬取
        "html": {
            "url": "http://forex.hexun.com/market/index-##page##.html",
            "filter": {

            },
            "css": ".mainboxcontent ul li",
            "regular": "",
            "my_filter": "MyFilter.rule_html_list",
            "store": "store_article_list",
            "recursive": {
                # 递归时配置
                "next_page": {
                    "css": "",
                    "my_filter": "rule_html_list_page"
                },
            }
        }
    },
    # 文章抓取规则
    "article": {
        "max_replicate": 4,  # 连续重复多少次则停止抓取url，0为不限 (重新抓取全部时则设置为0)
        "api": {
            # 暂无
        },
        "html": {
            # source http://www.neeq.com.cn/notice/20000482.html
            "source": "http://www.neeq.com.cn/notice/20000482.html",  # url来源：为空从数据库读取，不为空采用递归
            "filter": {

            },
            "css": ".newstext",  # 文章主体dom
            "regular": "",
            "my_filter": "rule_html_article",
            "store": "store_article",
            "recursive": {
                # 递归时的翻页配置
                "next_page": {
                    "css": ".next a",
                    "my_filter": "rule_html_article_page",
                },
                "max_num": 1,
            }
        }
    },
    # 文件抓取规则
    "file": {
        "basic_path": "./file/",
        "hash_path": "hash_path",
        "hash_filename": "hash_filename",
        "recursive": {
            # 递归时配置
            "next_page": {
                "css": "",
                "my_filter": "rule_file_page"
            },
            "max_num": 10,
        }
    }
}

config.update(conf)
print(config)

from cmspider.spider import Spider
s = Spider()
s.recover_status()
s.fetch_url()
s.fetch_file()
s.fetch_article()
