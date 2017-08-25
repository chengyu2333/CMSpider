import requests
import socket
import time
from cmspider.config import config
from cmspider.util import Util
from cmspider.url_manager import UrlManager
from urllib import request


class Fetch:
    __headers = config['basic']['header']
    __url_manager = UrlManager()
    socket.setdefaulttimeout(config['basic']['timeout'])

    def fetch_api(self, url, method="get", data=None, str_filter=None):
        try:
            if method == "get":
                data = requests.post(url, headers=self.__headers).text
            elif method == "post":
                data = requests.post(url, data, headers=self.__headers).text
            if str_filter:
                data = str_filter(data)
            return data
        except Exception as e:
            raise e
        finally:
            time.sleep(config['basic']['sleep'])

    def fetch_html(self, url):
        try:
            # if not util.url_filter(url):
            #     return
            html = requests.get(url, headers=self.__headers).content
            html = Util.html_decode(html)
            return html
        except Exception as e:
            raise e
        finally:
            time.sleep(config['basic']['sleep'])

    def fetch_file(self, url, filename):
        # if not os.path.exists(filename):
        #     os.makedirs(filename)
        try:
            req = request.Request(url, headers=self.__headers)
            data = request.urlopen(req).read()
            with open(filename, 'wb') as f:
                f.write(data)
                f.flush()
                f.close()
                self.__url_manager.set_url_status(url, 2)
        except Exception as e:
            self.__url_manager.set_url_status(url, -1)
            raise e
        finally:
            time.sleep(config['basic']['sleep'])
