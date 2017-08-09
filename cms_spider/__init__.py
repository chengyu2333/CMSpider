from cms_spider import config
import socket


conf = config.config

if __name__ == '__main__':
    print('初始化')
    socket.setdefaulttimeout(conf['basic']['timeout'])
