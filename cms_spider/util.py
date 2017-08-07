#!/usr/bin/python
# encoding: utf-8
import re
import sys
import platform
import hashlib


# 取文本中间
def get_str_middle(s, a, b):
    start = s.index(a)
    if start >= 0:
        start += len(a)
    end = s.index(b)
    return s[start:end]

# md5
def md5(obj):
    m = hashlib.md5()
    m.update(obj.encode())
    return m.hexdigest()


# Html解码
def html_decode(html):
    if "gbk" in str(html) or "gb2312" in str(html):
        return html.decode("gbk", errors="ignore")
    elif "utf-8" in str(html) or "UTF-8" in str(html):
        return html.decode("utf8", errors="ignore")
    else:
        return html


# 过滤url
def url_filter(url):
    try:
        # 外链
        if "http" in url and "hexun.com" in url:
            # 爬取层次
            if url.count("/") <= 4:
                return True
        else:
            return False
    except Exception as e:
        return False


# 进度条
def view_bar(num, total):
    # os.system('cls'.encode().decode("gbk"))
    num = int(num/total*50)
    total = 50
    rate = num / total
    rate_num = int(rate * 100)
    r = '\r[%s%s]%d%%  ' % ("="*num, " "*(50-num), rate_num, )
    sys.stdout.write(r)
    sys.stdout.flush()


def is_windows_system():
    return 'Windows' in platform.system()


def is_linux_system():
    return 'Linux' in platform.system()