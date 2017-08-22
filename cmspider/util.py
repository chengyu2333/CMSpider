import time
import sys
import platform
import hashlib


class Util:
    COUNT_PROCESSED = 0
    COUNT_SUCCESS = 0
    COUNT_DUPLICATE = 0
    COUNT_FAILED = 0


    # 语义指纹
    @staticmethod
    def duplicate(s):
        pass

    # 根据值查找键
    @staticmethod
    def get_dict_key(d, value):
        for k, v in d.items():
            if v == value:
                return k
        return None

    # 转成timestamp
    @staticmethod
    def get_timestamp(t, f='%Y-%m-%d %H:%M:%S'):
        tup = time.strptime(t, f)
        ts = time.mktime(tup)
        return ts

    # 取文本中间
    @staticmethod
    def get_str_middle(s, a, b):
        start = s.index(a)
        if start >= 0:
            start += len(a)
        end = s.index(b)
        return s[start:end]

    # md5
    @staticmethod
    def md5(obj):
        m = hashlib.md5()
        m.update(obj.encode())
        return m.hexdigest()

    # Html解码
    @staticmethod
    def html_decode(html):
        if "gbk" in str(html) or "gb2312" in str(html):
            return html.decode("gbk", errors="ignore")
        elif "utf-8" in str(html) or "UTF-8" in str(html):
            return html.decode("utf8", errors="ignore")
        else:
            return html

    # 进度条
    @staticmethod
    def view_bar(num, total):
        # os.system('cls'.encode().decode("gbk"))
        current = int(num/total*50)
        max_num = 50
        rate = num / total
        rate_num = rate * 100.0

        # print(Util.count, "  ", total_page)
        r = '\r[%s%s]%.2f%%  [%d/%d]' % ("="*current, " "*(max_num-current), rate_num, num, total)
        sys.stdout.write(r)
        sys.stdout.flush()

    @staticmethod
    def is_windows_system():
        return 'Windows' in platform.system()

    @staticmethod
    def is_linux_system():
        return 'Linux' in platform.system()