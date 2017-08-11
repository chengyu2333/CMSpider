from cmspider import DB
from cmspider import config
from pymongo import errors


class UrlManager:
    conf = config
    db = DB()
    con = db.get_mongodb_conn(conf['db']['table_list'])
    file_suffix = ["jpg","jpeg","png","doc","docx","xls","xlsx","ppt","pdf","zip","tar","rar","wps","txt"]

    # 添加url
    def put_url(self, url, title, timestamp=0.0, filetype=""):
        # 简单识别url类型
        suffix = url.split(".")[-1].split("?")[0]
        if not filetype:
            filetype = self.conf['list']['api']['filetype']
            for i in self.file_suffix:
                if i == suffix:
                    filetype = "file"
                    break
        # 如果有时间戳
        if timestamp:
            obj = {"title": title, "timestamp": timestamp, "_id": url, "type": filetype}
        else:
            obj = {"title": title, "_id": url, "type": filetype}

        try:
            return self.con.insert(obj)
        except errors.DuplicateKeyError as dk:
            raise dk
        except Exception as e:
            raise e

    # 设置url状态
    def set_url_status(self, url, status):
        try:
            return self.con.update({"_id": url}, {"$set": {"status": status}})
        except Exception as e:
            raise e

    # 获取url列表
    def get_url(self, num, file_type="html"):
        try:
            if file_type == "html":
                res = self.con.find({"$or": [{"status": {"$exists": False}}, {"status": 0}], "type": "html"}).limit(num)
            elif file_type == "file":
                res = self.con.find({"$or": [{"status": {"$exists": False}}, {"status": 0}], "type": "file"}).limit(num)
            else:
                raise Exception("文件类型错误")
        except Exception as e:
            raise e
        urls = []
        for url in res:
            self.set_url_status(url["_id"], 1)
            urls.append(url)
        return urls

    # 获取最新url
    def get_last_url(self, file_type="html"):
        try:
            if file_type == "html":
                res = self.con.find({"type": "html"}).sort('timestamp', -1).limit(1)
            elif file_type == "file":
                res = self.con.find({"type": "file"}).sort('timestamp', -1).limit(1)
            else:
                raise Exception("文件类型错误")
        except Exception as e:
            raise e
        return res[0]

    # 恢复全部状态
    def set_all_status(self, status=0):
        try:
            return self.con.update({}, {"$set": {"status": status}}, multi=True)
        except Exception as e:
            raise e
