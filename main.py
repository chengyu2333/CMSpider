from cms_spider import spider
from cms_spider import util

import io

config = io.open("config.json").read()
s = spider.Spider(config).run()