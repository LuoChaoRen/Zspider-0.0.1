import re,logging
import spider
import urllib.parse
class Parser(object):

    def working(self,task,spider_url,next_page_url,cookies):

        try:
            url, keys, contents,priority = task
            # contents = urllib.parse.unquote(content)
            re_group = re.compile(spider_url).findall(contents, re.IGNORECASE)
            url_set = {(spider.get_url_legal(_url,base_url=url)).split("#")[0] for _url in re_group}
            next_page_set = {__url for __url in url_set if re.compile(next_page_url).search(__url)}
            flter_url_set = [url_set.remove(_url) for _url in next_page_set if _url in url_set]
            if next_page_url:
                next_url_re_group = re.compile(next_page_url).findall(contents, re.IGNORECASE)
                add_set = [next_page_set.add((spider.get_url_legal(_url,base_url=url)).split("#")[0]) for _url in next_url_re_group]
            state, item = self.htm_parse(url, contents,cookies)
            key = {"type":"parser"}
        except Exception as excep:
            next_page_set = {}
            url_set = {}
            item =None
            state = 0
            key = {"type":"parser"}
            logging.error("parer:",excep)
        return next_page_set,url_set,key,state,item

    def htm_parse(self, url: str, content: object,cookies:dict) -> (int,dict):
        """
        :param url:请求的url
        :param content:请求返回的response.text
        :return:提取状态:state(int) 不为0即为成功,提取到的需要的结果:item(dict)
        """
        raise NotImplementedError
