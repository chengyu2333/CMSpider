from pymongo import MongoClient
from pymongo import errors
from cms_spider import config


class DB:
    conf = config.config
    db = None
    table = None

    def __init__(self):
        client = MongoClient(self.conf['db']['host'], self.conf['db']['port'])
        self.db = client[self.conf['db']['db_name']]

    # 写入数据
    def put_data(self, data, table_name):
        print(data)
        try:
            con = self.db[table_name]
            return con.insert(data)
        except Exception as e:
            raise e

    # 获取连接
    def get_conn(self, table_name):
        return self.db[table_name]
