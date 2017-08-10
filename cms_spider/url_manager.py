import cms_spider
from cms_spider import database
from cms_spider import config
import pymongo
from pymongo import errors

conf = config.config
db = database.DB()
con = db.get_mongodb_conn(conf['db']['table_list'])
file_suffix = ["jpg","jpeg","png","doc","docx","xls","xlsx","ppt","pdf","zip","tar","rar","wps","txt"]


# 添加url
def put_url(url, title, timestamp=0.0, filetype=""):
    filetype = conf['list']['api']['filetype']
    # 简单识别url类型
    suffix = url.split(".")[-1].split("?")[0]
    if not filetype:
        filetype = "html"
        for i in file_suffix:
            if i == suffix:
                filetype = "file"
                break

    if timestamp:
        obj = {"title": title, "timestamp": timestamp, "_id": url, "type": filetype}
    else:
        obj = {"title": title, "_id": url, "type": filetype}

    try:
        return con.insert(obj)
    except errors.DuplicateKeyError as dk:
        raise dk
    except Exception as e:
        raise e


# 设置url状态
def set_url(url, status):
    try:
        return con.update({"_id": url}, {"$set": {"status": status}})
    except Exception as e:
        raise e


# 获取url列表
def get_url(num, type="html"):
    try:
        if type=="html":
            res = con.find({"$or": [{"status": {"$exists": False}}, {"status": 0}], "type": "html"}).limit(num)
        elif type=="file":
            res = con.find({"$or": [{"status": {"$exists": False}}, {"status": 0}], "type": "file"}).limit(num)
        else:
            raise Exception("文件类型错误")
    except Exception as e:
        raise e
    urls = []
    for url in res:
        set_url(url["_id"], 1)
        urls.append(url)
    return urls


# 获取最新url
def get_last_url(type="html"):
    try:
        if type=="html":
            res = con.find({"type": "html"}).sort('timestamp', -1).limit(1)
        elif type=="file":
            res = con.find({"type": "file"}).sort('timestamp', -1).limit(1)
        else:
            raise Exception("文件类型错误")
    except Exception as e:
        raise e
    return res[0]


# 恢复全部状态
def recover_status():
    try:
        return con.update({}, {"$set": {"status": 0}}, multi=True)
    except Exception as e:
        raise e
