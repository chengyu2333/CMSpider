from pymongo import MongoClient
from cmspider import config


class DB:
    conf = config
    db = None
    table = None

    def __init__(self):
        client = MongoClient(self.conf['db']['host'], self.conf['db']['port'])
        self.db = client[self.conf['db']['db_name']]

    # 获取连接
    def get_mongodb_conn(self, table_name):
        return self.db[table_name]
