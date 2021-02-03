
def test():
    spidername = "xxx"
    start_url = "xxx"
    white_list = "re.xxxx"
    #初始化爬虫
    webSpider = webSpider()
    webSpider.spider_ini(spidername,start_url,white_list)
    webSpider.method(myparser,mysent,mylogin)
    webSpider.start()