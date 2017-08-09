from cms_spider import catch
from cms_spider import exception
from cms_spider import config
from cms_spider import my_store
from cms_spider import filter
from pymongo import errors
from cms_spider import url_manager
conf = config.config
DUPLICATE_COUNT = 0


# 抓取一页列表
def catch_list_one(page):
    global DUPLICATE_COUNT
    try:
        if "rule_api" in conf:
            # 通过api获取
            c = conf['rule_api']['list']
            res = catch.catch_api(c['url'], method=c['method'], data=c['args'])
            res = conf['rule_api']['list']['my_filter'](res)
            my_store.store_list(res)
            return res
        elif "rule_html" in conf:
            # 通过HTML获取
            c = conf['rule_html']['list']
            res = catch.catch_html(c['url'])
            res = filter.dom_filter(res, conf['rule_html']['list']['css'], conf['rule_html']['list']['my_filter'])
            my_store.store_list(res)
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
def catch_list_multi():
    global DUPLICATE_COUNT
    start = conf['basic']['start_page']
    i = int(start)
    max_page = int(conf['basic']['max_page'])
    page_key = ""

    # 组合page参数
    if "rule_api" in conf:  # api
        if conf['rule_api']['list']['url'].find("##page##") >= 1:  # get
            page_key = "##inurl##"
            url = conf['rule_api']['list']['url'].split("##page##")
        else:  # post
            page_key = config.get_dict_key(conf['rule_api']['list']['args'], "##page##")
    elif "rule_html" in conf:  # html
        if conf['rule_html']['list']['url'].find("##page##") >= 1:
            page_key = "##inurl##"
            url = conf['rule_html']['list']['url'].split("##page##")
    else:
        raise Exception("列表抓取规则配置错误")

    while True:
        total = int(conf['basic']['total_page'])

        # 超过重复次数
        rep = True
        if conf['basic']['max_replicate']:
            rep = conf['basic']['max_replicate'] >= DUPLICATE_COUNT

        # 达到最新地址
        # url_manager.get_last_url()

        # 开始抓取
        if i <= max_page and i <= total and rep:  # 范围
            if page_key:
                # 组合URL
                if "rule_api" in conf:  # api
                    if page_key == "##inurl##":  # get
                        conf['rule_api']['list']['url'] = url[0] + str(i) + url[1]
                        print(conf['rule_api']['list']['url'])
                    else:  # post
                        conf['rule_api']['list']['args'][page_key] = str(i)
                elif "rule_html" in conf:  # html
                    if page_key == "##inurl##":
                        conf['rule_html']['list']['url'] = url[0] + str(i) + url[1]
                        print(conf['rule_html']['list']['url'])
            try:
                catch_list_one(i)
                i += 1
            except exception.ListFinishedException:
                print('URL更新完成，数量:', i)
                break

        else:
            print('URL抓取完成')
            break
