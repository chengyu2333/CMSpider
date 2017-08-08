from cms_spider import database
from cms_spider import config

conf = config.config
db = database.DB()
con = db.get_mongodb_conn(conf['db']['table_list'])


# 添加url
def put_url(url, title):
    try:
        obj = {"title": title, "_id": url}
        return con.insert(obj)
    except Exception as e:
        raise e


# 设置url状态
def set_url(url, status):
    try:
        return con.update({"_id": url}, {"$set": {"status": status}})
    except Exception as e:
        raise e


# 获取url列表
def get_url(num):
    try:
        res = con.find({"$or": [{"status": {"$exists": False}}, {"status": 0}]}).limit(num)
    except Exception as e:
        raise e
    urls = []
    for url in res:
        set_url(url["_id"], 1)
        urls.append(url)
    return urls


# 恢复全部状态
def recover_status():
    try:
        return con.update({"status": {"$gt": 0}}, {"$set": {"status": 0}}, multi=True)
    except Exception as e:
        raise e

