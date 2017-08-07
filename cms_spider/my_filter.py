# 自定义过滤函数
from cms_spider import util


def rule_api_list(s):
    return s[6:-2]


def rule_html_column(s):
    return s


def rule_html_list(s):
    return s


def rule_html_list_page(s):
    return s


def rule_html_article(s):
    return s


def rule_html_article_page(s):
    return s


def rule_file_page(s):
    return s