from cms_spider import spider
from cms_spider import util
import socket


socket.setdefaulttimeout(5)
s = spider.Spider()
# s.catch_url()
s.catch_article()