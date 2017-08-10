# 自定义过滤函数
import hashlib
from bs4 import BeautifulSoup
import re


class Filter:
    # 补全url
    @staticmethod
    def completion_url(target_url, example_url):
        if "http" in target_url:
            return target_url
        else:
            example_url = example_url.split("/")
            return example_url[0]+"//"+example_url[2]+"/"+target_url

    # 过滤url
    @staticmethod
    def url_filter(url):
        if re.match(r'^https?:/{2}\w.+$', url):
            # 层次
            # if url.count("/") > 4:
            #     return False
            return True
        return False

    @staticmethod
    def dom_filter(html, css="", func=None):
        try:
            html = BeautifulSoup(html, "html5lib")
            html = html.select(css)
            if func:
                html = func(html)
            return html
        except Exception:
            raise

    # hash路径
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
        return s

    @staticmethod
    def rule_html_article_page(s):
        return s

    @staticmethod
    def rule_file_page(s):
        return s
