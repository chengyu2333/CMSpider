import hashlib
from cmspider import Util
from bs4 import BeautifulSoup


class MyFilter:
    # def __init__(self, string, conf_rule):
        # super(MyFilter, self).__init__(string, conf_rule)

    # 文件hash路径
    @staticmethod
    def hash_path(source):
        m = hashlib.md5()
        m.update(source.encode())
        h = m.hexdigest()
        hash_p = h[0:2] + "/" + h[2:4] + "/"
        return hash_p

    # hash文件名
    @staticmethod
    def hash_filename(source):
        return source

    # api获取的list过滤
    @staticmethod
    def rule_api_list(s):
        return s[6:-2]

    @staticmethod
    def rule_html_column(s):
        return s

    @staticmethod
    def rule_html_list(s):
        for i in s:
            i.text
        return s

    @staticmethod
    def rule_html_list_page(s):
        return s

    @staticmethod
    def rule_html_article(s):
        s = s[0]
        title = s.select("h3")[0].text
        info = s.select(".info")[0].text
        time = Util.get_str_middle(info,"发布时间："," 点击次数")
        content = s.select(".txt")[0]

        s = {"title": title, "time": time, "content": str(content)}
        return s

    @staticmethod
    def rule_html_article_page(s):
        return s

    @staticmethod
    def rule_file_page(s):
        return s
