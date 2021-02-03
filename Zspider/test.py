import spider
import re,time
import logging
import lxml.html
etree = lxml.html.etree
class MyRequester(spider.Requests):
    def Request(self,session,page_url,parser_url,proxy) -> (int,str,str):
        #根据url/keys进行精准过滤,请求
        if page_url:
            response = session.get(page_url)
            print("page_url:",page_url)
        else:
            response = session.get(parser_url)
            print("parser_url:", page_url)
        return int(response.status_code),response.url,response.text

class MyParser(spider.Parser):
    def htm_parse(self,url,content) -> (int, dict):
        html = etree.HTML(content)
        title = html.xpath("//div[@id='topics']//h1[@class='postTitle']/a/span/text()")
        item = {
            "title":title,
            "url": url
        }
        return 1,item
class MySaver(spider.Save):
    def item_save(self,item) -> (int,str):
        #如何存储  返回 save_state(int), save_result(str)
        return 1 , "1"

class MySenter(spider.Sent):
    def sent_get(self) -> (str,dict,dict,str):
        """
        需要登录
        需要return request_url,request_header,request_data,request_method
        """
        request_url = "https://www.baidu.com"
        request_header = None
        request_data = None
        request_method = "get"
        return request_url,request_header,request_data,request_method
myrequest = MyRequester()
myparser = MyParser()
mysaver = MySaver()
mysent = MySenter(10)#设置时间间隔
def test():
    """
    爬虫名称 spidername
    起始url start_url
    需要爬取的url spider_url
    下一页url   next_page_url
    """
    spidername = "cnblogs"
    start_url = "https://www.cnblogs.com/"
    spider_url  =  r'(https://www\.cnblogs\.com\/[^\s]*/p/[^\s]*)"'
    next_page_url = r"/sitehome/p/\d+"
    #初始化爬虫
    webSpider = spider.ini_Spider()
    webSpider.spider_ini(name=spidername,start_url=start_url,spider_url=spider_url,next_page_url=next_page_url)
    webSpider.method(requester=myrequest ,parser=myparser,save=mysaver,sent=mysent)
    webSpider.start()

test()