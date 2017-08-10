from bs4 import BeautifulSoup
import re


def dom_filter(html, css="", func=None):
    try:
        html = BeautifulSoup(html, "html5lib")
        html = html.select(css)
        if func:
            html = func(html)
        return html
    except Exception:
        raise


# 补全url
def completion_url(target_url, example_url):
    if "http" in target_url:
        return target_url
    else:
        example_url = example_url.split("/")
        return example_url[0]+"//"+example_url[2]+"/"+target_url


# 过滤url
def url_filter(url):
    if re.match(r'^https?:/{2}\w.+$', url):
        # 层次
        # if url.count("/") > 4:
        #     return False
        return True
    return False


# 语义指纹
def duplicate(s):
    pass
