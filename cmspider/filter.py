from cmspider import MyFilter
from cmspider import MyStore
from bs4 import BeautifulSoup
import re


class Filter(MyStore):
    __result = None
    __store = MyStore()
    __conf = None

    def __init__(self, string="", conf_rule=None):
        self.__conf = conf_rule
        if conf_rule and string:
            if "css" in conf_rule and conf_rule['css']:
                self.__result = self.dom_filter(string, conf_rule['css'])
            if"regular" in conf_rule and conf_rule['regular']:
                self.__result = self.reg_filter(string, conf_rule['regular'])
            if "my_filter" in conf_rule and conf_rule['my_filter']:
                if self.__result:
                    self.__result = eval("MyFilter."+conf_rule['my_filter'])(self.__result)
                else:
                    self.__result = eval("MyFilter."+conf_rule['my_filter'])(string)

    def store(self, table, url=""):
        try:
            if table == "list":
                eval("self."+self.__conf['store'])(self.__result)
            elif table == "article":
                eval("self." + self.__conf['store'])(self.__result, url)
        except Exception as e:
            raise


    # def store_list(self):
    #     try:
    #         eval("self.__store."+self.__conf['store'])(self.__result)
    #     except Exception:
    #         raise
    #
    # def store_article(self, url):
    #     try:
    #         self.__store.eval(self.__conf['store'])(self.__result, url)
    #     except Exception:
    #         raise

    def get_result(self):
        return self.__result

    def dom_filter(self, html_str, css=""):
        try:
            if self.__result:
                data = self.__result
            else:
                data = html_str
            data = BeautifulSoup(data, "html5lib")
            data = data.select(css)
            # print(str(data[0]))
            self.__result = data
            return data
        except Exception:
            raise

    def reg_filter(self, string, p):
        res = []
        if self.__result:
            data = str(self.__result)
        else:
            data = string
        for item in data:
            # self.__result = re.findall(p, data)
            # print(re.findall(p, item))
            res.append(re.findall(p, str(item)))
        return res

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


