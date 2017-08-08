from cms_spider import config
from cms_spider import util
from cms_spider import filter
from urllib import request
from bs4 import BeautifulSoup
import requests
import socket

conf = config.config
headers = conf['basic']['header']
socket.setdefaulttimeout(conf['basic']['timeout'])


def catch_api(url, method="get", data=None, str_filter=None):
    try:
        if method == "get":
            data = requests.post(url, headers=headers).text
        elif method == "post":
            data = requests.post(url, data, headers=headers).text
        if str_filter:
            data = str_filter(data)
        return data
    except Exception as e:
        raise e


def catch_html(url):
    try:
        # if not filter.url_filter(url):
        #     return
        html = requests.get(url, headers=headers).content
        html = util.html_decode(html)
        return html
    except Exception as e:
        raise e


def catch_file(url, filename):
    try:
        req = request.Request(url, headers=headers)
        data = request.urlopen(req).read()
        with open(filename, 'wb') as f:
            f.write(data)
            f.flush()
            f.close()
    except Exception as e:
        raise e
