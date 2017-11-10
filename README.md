# CMSpider
一个针对CMS结构网站的分布式通用爬虫框架

# feathers
- 可爬取API
- 可以爬网页的正文或文件
- 自动处理翻页
- 只需要改改配置文件即可爬取大多数结构的网站
- 分布式架构，使用celery调度

### Config example
```
# from cmspider import MyFilter

# 说明：
# 1.使用##page##来标记页码
# 2.匹配规则css、filter将会依次应用在源数据中

config = {
    # 数据库配置
    "db": {
        "type": "mongodb",
        "host": "127.0.0.1",
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
        "base_url": "neeq.com.cn",
        "start_page": 0,  # 起始页
        "max_page": 999,  # 最多爬取的页数
        "total_page": 10,  # 网站总页数,动态获取
        "start_date": "",  # 开始日期
        "end_date": "",  # 结束日期
        "max_replicate": 0,  # 连续重复多少次则停止抓取url，0为不限，
        "print_log": True
    },
    # 板块（API）抓取规则
    "column": {
        "css": "",
        "my_filter": "MyFilter.rule_html_column"
    },
    # 待爬URL抓取规则
    "list": {
        # 通过api获取
        "api": {
            # "filetype": "file",  # html | file
            "method": "post",
            "url": "http://www.neeq.com.cn/disclosureInfoController/infoResult.do",
            # POST数据
            "post_data": {
                "disclosureType": "6",
                "page": "##page##",
                "isNewThree": "1",
                "startTime": "2016-08-07",
                "endTime": "2017-08-07",
            },
            "my_filter": "rule_api_list",
            "store": "store_file_list"
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
            "page": {
                # 递归时配置
                "next_page": {
                    "css": "",
                    "my_filter": "rule_html_list_page"
                },
                "page_list": {
                }
            }
        },
        "store": {
            # 存储映射
            "map": {
                "css": "db_field"
            }
        }
    },
    # 正文抓取规则
    "article": {
        "api": {
        },
        "html": {
            # http://www.neeq.com.cn/notice/20000477.html
            "source": "",  # url来源：为空从数据库读取，不为空采用递归
            "filter": {

            },
            "css": ".newstext",  # 文章主体dom
            "regular": "",
            "my_filter": "rule_html_article",
            "store": "store_article",
            "max_num": 1,
            "page": {
                # 递归时配置
                "next_page": {
                    "css": ".next a",
                    "my_filter": "rule_html_article_page",
                }
            }
        }
    },
    # 文件抓取规则
    "file": {
        "basic_path": "./file/",
        "hash_path": "hash_path",
        "hash_filename": "hash_filename",
        # "store": "store_article_list",
        "max_num": 10,
        "page": {
            # 递归时配置
            "next_page": {
                "css": "",
                "my_filter": "rule_file_page"
            }
        }
    }
}
```
