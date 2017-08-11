from pymongo import MongoClient
from cmspider import config


class DB:
    __db = None
    __table = None

    def __init__(self):
        client = MongoClient(config['db']['host'], config['db']['port'])
        self.__db = client[config['db']['db_name']]

    # 获取连接
    def get_mongodb_conn(self, table_name):
        return self.__db[table_name]

    def put_article(self, article_data):
        try:
            self.__db[config['db']['table_article']].insert(article_data)
        except Exception:
            raise
