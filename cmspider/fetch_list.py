from cmspider import Fetch
from cmspider import exception
from cmspider import config
from cmspider import Store
from cmspider import Filter
import cmspider
from pymongo import errors

store = Store()


class FetchList(Fetch):
    duplicate_count = 0

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
            self.duplicate_count = 0
        except errors.DuplicateKeyError as e:
            self.duplicate_count += 1
            print("\r重复url " + str(self.duplicate_count), end="")
        except exception.ListFinishedException as f:
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
                page_mark = cmspider.Util.get_dict_key(config['list']['api']['post_data'], "##page##")
        elif "html" in config['list']:  # html
            if config['list']['html']['url'].find("##page##") >= 1:
                page_mark = "##inurl##"
                url = config['list']['html']['url'].split("##page##")
        else:
            raise Exception("列表抓取规则配置错误")

        while True:
            total = int(config['basic']['total_page'])

            # 超过连续重复次数
            rep = True
            if config['basic']['max_replicate']:
                rep = config['basic']['max_replicate'] >= self.duplicate_count

            # 达到最新地址
            # self.url_manager.get_last_url()
            # raise exception.ListFinishedException

            # 开始抓取
            if i <= max_page and i <= total and rep:  # 范围
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
                except exception.ListFinishedException:
                    print('\nURL更新完成，数量:', i-int(start))
                    break
                except Exception:
                    raise
            else:
                print('\n全部URL抓取完成')
                break
