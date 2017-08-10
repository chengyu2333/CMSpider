from cmspider import Fetch
from cmspider import exception
from cmspider import config
from cmspider import Store
from cmspider import my_filter
import cmspider
from pymongo import errors
conf = config
DUPLICATE_COUNT = 0

store = Store()
# 抓取单页列表
def fetch_list_one(page):
    global DUPLICATE_COUNT
    try:
        if "api" in conf['list']:
            # 通过api获取
            c = conf['list']['api']
            res = Fetch().fetch_api(c['url'], method=c['method'], data=c['args'])
            res = conf['list']['api']['my_filter'](res)
            store.store_list(res)
            return res
        elif "html" in conf['list']:
            # 通过HTML获取
            c = conf['list']['html']
            res = Fetch.fetch_html(c['url'])
            res = my_filter.dom_filter(res, conf['list']['html']['css'], conf['list']['html']['my_filter'])
            store.store_list(res)
            return res
        else:
            raise Exception("列表抓取规则配置错误")
        DUPLICATE_COUNT = 0
    except errors.DuplicateKeyError as e:
        DUPLICATE_COUNT += 1
        print("\r重复url "+str(DUPLICATE_COUNT), end="")
    except exception.ListFinishedException as f:
        raise f


# 批量抓取列表
def fetch_list_multi(max_dup=0):
    global DUPLICATE_COUNT
    start = conf['basic']['start_page']
    i = int(start)
    max_page = int(conf['basic']['max_page'])
    page_mark = ""

    # 组合page参数
    if "api" in conf['list']:  # api
        if conf['list']['api']['url'].find("##page##") >= 1:  # get
            page_mark = "##inurl##"
            url = conf['list']['api']['url'].split("##page##")
        else:  # post
            page_mark = cmspider.Util.get_dict_key(conf['list']['api']['args'], "##page##")
    elif "html" in conf['list']:  # html
        if conf['list']['html']['url'].find("##page##") >= 1:
            page_mark = "##inurl##"
            url = conf['list']['html']['url'].split("##page##")
    else:
        raise Exception("列表抓取规则配置错误")

    while True:
        total = int(conf['basic']['total_page'])

        # 超过连续重复次数
        rep = True
        if conf['basic']['max_replicate']:
            rep = conf['basic']['max_replicate'] >= DUPLICATE_COUNT

        # 达到最新地址
        # url_manager.get_last_url()

        # 开始抓取
        if i <= max_page and i <= total and rep:  # 范围
            if page_mark:
                # 组合URL
                if "api" in conf['list']:  # api
                    if page_mark == "##inurl##":  # get
                        conf['list']['api']['url'] = url[0] + str(i) + url[1]
                        print(conf['list']['api']['url'])
                    else:  # post
                        conf['list']['api']['args'][page_mark] = str(i)
                elif "html" in conf['list']:  # html
                    if page_mark == "##inurl##":
                        conf['list']['html']['url'] = url[0] + str(i) + url[1]
                        print(conf['list']['html']['url'])
            try:
                fetch_list_one(i)
                i += 1
            except exception.ListFinishedException:
                print('URL更新完成，数量:', i)
                break
        else:
            print('全部URL抓取完成')
            break
