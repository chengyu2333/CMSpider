from bs4 import BeautifulSoup
from cms_spider import my_filter


def dom_filter(html, css="", func=None):
    try:
        html = BeautifulSoup(html, "html5lib")
        html = html.select(css)
        if func:
            html = func(html)
        return html
    except Exception as e:
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
    try:
        # 外链
        if "http" in url:
            # url层次
            if url.count("/") <= 4:
                return True
        else:
            return False
    except Exception as e:
        return False


# 语义指纹
def duplicate(s):
    pass
