#!/usr/bin/python
# encoding: utf-8
import time
import sys
import platform
import hashlib


# 根据值查找键
def get_dict_key(d, value):
    for k, v in d.items():
        if v == value:
            return k
    return None


# 转成timestamp
def get_timestamp(t, f='%Y-%m-%d %H:%M:%S'):
    tup = time.strptime(t, f)
    ts = time.mktime(tup)
    return ts


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