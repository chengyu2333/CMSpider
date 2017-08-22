from cmspider.fetch import Fetch
from cmspider.config import config
from cmspider.url_manager import UrlManager
from cmspider.my_filter import MyFilter
import os


class FetchFile(Fetch):
    __url_manager = UrlManager()

    def __init__(self):
        pass

    def fetch_file_single(self, url_obj):
        path = config['file']['basic_path'] + eval("MyFilter."+config['file']['hash_path'])(url_obj["_id"])
        if not os.path.exists(path):
            os.makedirs(path)
        filename = url_obj["_id"].split(".")[-1].split("?")[0]
        full_path = path + url_obj['title'] + "." + eval("MyFilter."+config['file']['hash_filename'])(filename)
        print("\r" + full_path, end="")
        Fetch().fetch_file(url_obj['_id'], full_path)

    def fetch_file_multi(self):
        while True:
            urls = self.__url_manager.get_url(file_type="file")
            if not urls:
                break
            for url_obj in urls:
                self.fetch_file_single(url_obj)
