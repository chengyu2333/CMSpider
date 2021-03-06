from cmspider.fetch import Fetch
from cmspider import exception
from cmspider.config import config
from cmspider.store import Store
from cmspider.filter import Filter
from cmspider.util import Util
from pymongo import errors


class FetchList(Fetch):
    __store = Store()
    __filter = Filter()

    # 抓取单页列表
    def fetch_list_one(self, page):
        try:
            if "api" in config['list']:
                # 通过api获取
                c = config['list']['api']
                res = self.fetch_api(c['url'], method=c['method'], data=c['post_data'])
                Filter(res, config['list']['api']).store("list")
                return res
            elif "html" in config['list']:
                # 通过HTML获取
                c = config['list']['html']
                res = self.fetch_html(c['url'])
                Filter(res, config['list']['html']).store("list")
                return res
            else:
                raise Exception("列表抓取规则配置错误")
        except exception.ExceedMaxDuplicate as f:
            raise f

    # 批量抓取列表
    def fetch_list_multi(self, max_dup=0):
        start = config['basic']['start_page']
        i = int(start)
        max_page = int(config['basic']['max_page'])
        page_mark = ""

        # 组合page参数
        if "api" in config['list']:  # api
            if config['list']['api']['url'].find("##page##") >= 1:  # get
                page_mark = "##inurl##"
                url = config['list']['api']['url'].split("##page##")
            else:  # post
                page_mark = Util.get_dict_key(config['list']['api']['post_data'], "##page##")
        elif "html" in config['list']:  # html
            if config['list']['html']['url'].find("##page##") >= 1:
                page_mark = "##inurl##"
                url = config['list']['html']['url'].split("##page##")
        else:
            raise Exception("列表抓取规则配置错误")

        while True:
            total = int(config['basic']['total_page'])

            # 开始批量抓取
            if i <= max_page and i <= total:  # 范围
                if page_mark:
                    # 组合URL
                    if "api" in config['list']:  # api
                        if page_mark == "##inurl##":  # get
                            config['list']['api']['url'] = url[0] + str(i) + url[1]
                            print(config['list']['api']['url'])
                        else:  # post
                            config['list']['api']['post_data'][page_mark] = str(i)
                    elif "html" in config['list']:  # html
                        if page_mark == "##inurl##":
                            config['list']['html']['url'] = url[0] + str(i) + url[1]
                            print(config['list']['html']['url'])
                try:
                    self.fetch_list_one(i)
                    i += 1
                except exception.ExceedMaxDuplicate:
                    print('\n增量URL更新完成，数量:', Util.COUNT_SUCCESS)
                    break
                except Exception:
                    raise
            else:
                print('\n抓取全部URL完成,数量:', Util.COUNT_SUCCESS)
                break
