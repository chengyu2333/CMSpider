import cmspider
from cmspider import config
from cmspider import Util
from urllib import request
import requests
import socket
import os


class Fetch:
    conf = config
    headers = conf['basic']['header']
    socket.setdefaulttimeout(conf['basic']['timeout'])
    url_manager = cmspider.UrlManager()

    def fetch_api(self, url, method="get", data=None, str_filter=None):
        try:
            if method == "get":
                data = requests.post(url, headers=self.headers).text
            elif method == "post":
                data = requests.post(url, data, headers=self.headers).text
            if str_filter:
                data = str_filter(data)
            return data
        except Exception as e:
            raise e

    def fetch_html(self, url):
        try:
            # if not util.url_filter(url):
            #     return
            html = requests.get(url, headers=self.headers).content
            html = Util.html_decode(html)
            return html
        except Exception as e:
            raise e

    def fetch_file(self, url, filename):
        # if not os.path.exists(filename):
        #     os.makedirs(filename)
        try:
            req = request.Request(url, headers=self.headers)
            data = request.urlopen(req).read()
            with open(filename, 'wb') as f:
                f.write(data)
                f.flush()
                f.close()
                self.url_manager.set_url_status(url, 2)
        except Exception as e:
            self.url_manager.set_url_status(url, -1)
            raise e
