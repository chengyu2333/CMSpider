# 自定义过滤函数
import hashlib


# hash路径
def hash_path(source):
    m = hashlib.md5()
    m.update(source.encode())
    h = m.hexdigest()
    hash_p = h[0:2] + "/" + h[2:4] + "/"
    return hash_p


# hash文件名
def hash_filename(source):
    return source


def rule_api_list(s):
    return s[6:-2]


def rule_html_column(s):
    return s


def rule_html_list(s):
    for i in s:
        i.text
    return s


def rule_html_list_page(s):
    return s


def rule_html_article(s):
    return s


def rule_html_article_page(s):
    return s


def rule_file_page(s):
    return s