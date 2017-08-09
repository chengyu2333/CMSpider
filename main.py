from cms_spider import spider
from cms_spider import util


s = spider.Spider()
s.recover_status()
s.catch_url()
# s.catch_file()