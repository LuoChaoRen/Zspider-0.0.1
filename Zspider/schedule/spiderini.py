# _*_ coding: utf-8 _*_
from schedule.cthreads.utilities.util_urlfilter import UrlFilter
from .threads_pool import ThreadPool
import re

#爬虫初始化
class ini_Spider(object):

    def __init__(self):
        self.urlfilter = ""
        self.start_url = ""
        self.spider_url = ""
        self.next_page_url = ""
        self.web_spider = None
        return

    def spider_ini(self,name,start_url,spider_url,next_page_url):
        self.urlfilter = UrlFilter(white_patterns=(re.compile(spider_url), ), capacity=None)
        self.start_url = start_url
        self.spider_url = spider_url
        self.next_page_url = next_page_url
        return

    def method(self,parser=None, save=None, sent=None,requester=None,login=None):
        self.web_spider = ThreadPool(parser, save, sent,requester,login,url_filter=self.urlfilter)
        self.web_spider.set_start_url(self.start_url, keys={"type": "index"})

    def start(self,request_num=10):
        try:
            self.web_spider.start_working(request_num,self.spider_url,self.next_page_url)
        except:
            print("spider end")
