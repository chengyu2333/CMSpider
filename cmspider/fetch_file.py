from cmspider import Fetch
from cmspider import config
from cmspider import MyFilter
import os


class FetchFile(Fetch):
    def __init__(self):
        pass

    def fetch_file(self, url_obj):
        path = config['file']['basic_path'] + eval("MyFilter."+config['file']['hash_path'])(url_obj["_id"])
        if not os.path.exists(path):
            os.makedirs(path)
        filename = url_obj["_id"].split(".")[-1].split("?")[0]
        full_path = path + url_obj['title'] + "." + eval("MyFilter."+config['file']['hash_filename'])(filename)
        print("\r" + full_path, end="")
        Fetch().fetch_file(url_obj['_id'], full_path)