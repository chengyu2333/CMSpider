from cmspider.my_filter import Filter
from cmspider.config import config
from cmspider import exception
from cmspider.util import Util
from cmspider.database import DB
from cmspider.url_manager import UrlManager
from cmspider.my_store import Store
from cmspider.fetch import Fetch
from cmspider.spider import Spider
import socket

conf = config

if __name__ == '__main__':
    print('初始化')
    socket.setdefaulttimeout(conf['basic']['timeout'])








