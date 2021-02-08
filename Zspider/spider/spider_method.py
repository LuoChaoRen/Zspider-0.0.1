import spider
import re,time
import logging
import requests
import json
import random
import lxml.html
etree = lxml.html.etree


class DoLogin(spider.Login):
    def do_login(self) ->(dict):
        login = spider.Login163("luotao202013", "luotao2020123")
        result = login.start_login()
        return result

class MyRequester(spider.Requests):
    def Request(self,page_url,parser_url,cookie,proxy) -> (int,str,str):
        #根据url/keys进行精准过滤,请求"&func=global:sequential"
        if cookie["Coremail.sid"]:
            random3_str = ''.join(str(i) for i in random.sample(range(0, 9), 3))
            random5_str = ''.join(str(i) for i in random.sample(range(0, 9), 5))
            s = requests.session()
            s.keep_alive = False
            request_url = page_url + cookie["Coremail.sid"] + "&func=mbox:listMessages&Js6PromoteScriptLoadTime=1775&welcome_yx_red=1&mbox_folder_enter=1&stay_module=welcome," + str(int(round(time.time() * 1000)) - int(random3_str)) + "," + str(int(round(time.time() * 1000))) + "," + random5_str
            response = requests.post(url=request_url,cookies=cookie)
            status_code = int(response.status_code)
            print(status_code)
            if int(response.status_code) == 202:
                status_code = 0
            return status_code , response.url, response.text
        else:
            return 0, None, None


class MyParser(spider.Parser):
    def htm_parse(self,url,content,cookie) -> (int, dict):
        item = {}
        var_name_id = re.findall('.*<string name="id">(.*?)</string>.*', content)
        for im in var_name_id:
            request_var = {
                "var": '<?xml version="1.0"?><object><string name="id">' + im + '</string><boolean name="header">true</boolean><boolean name="returnImageInfo">true</boolean><boolean name="returnAntispamInfo">true</boolean><boolean name="autoName">true</boolean><object name="returnHeaders"><string name="Resent-From">A</string><string name="Sender">A</string><string name="List-Unsubscribe">A</string><string name="Reply-To">A</string></object><boolean name="supportTNEF">true</boolean></object>'
            }
            request_urls = "https://mail.163.com/js6/s?sid=" + cookie[
                "Coremail.sid"] + "&func=mbox:readMessage&l=read&action=read"
            r_info = requests.post(url=request_urls, data=request_var, cookies=cookie)
            user_from_data = re.findall('.*<array name="from">\n<string>(.*?)&lt;(.*?)&gt;</string>.*', r_info.text)
            user_to_data = re.findall('.*<array name="to">\n<string>(.*?)&lt;(.*?)&gt;</string>.*', r_info.text)
            if user_from_data:
                user_from = user_from_data[0][0]  # name
                from_email = user_from_data[0][1]  # mail
            else:
                user_from_data = re.findall('.*<array name="from">\n<string>((.*?)@.*)</string>.*', r_info.text)
                user_from = user_from_data[0][1]  # name
                from_email = user_from_data[0][0]  # mail
            if user_to_data:
                user_to = user_to_data[0][0]  # name
                to_email = user_to_data[0][1]  # mail
            else:
                user_to_data = re.findall('.*<array name="to">\n<string>((.*?)@.*)</string>.*', r_info.text)
                user_to = user_to_data[0][1]  # name
                to_email = user_to_data[0][0]  # mail

            subject = re.findall('.*<string name="subject">(.*?)</string>.*', r_info.text)[0]
            item[subject] = subject
        print(item)
        return 1,item
class MySaver(spider.Save):
    def item_save(self,item) -> (int,str):
        #如何存储  返回 save_state(int), save_result(str)
        return 1 , "1"

class MySenter(spider.Sent):
    def sent_get(self,cookie) -> (str,dict,dict,str):
        """
        需要登录
        需要return request_url,request_header,request_data,request_method
        """
        request_url = "https://mail.163.com/js6/s?sid="+ cookie["Coremail.sid"]+"&func=global:sequential"
        request_header = {
            "Host": "mail.163.com",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0",
            "Accept": "text/javascript",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-type": "application/x-www-form-urlencoded",
            "Content-Length": "1746",
            "Origin": "https://mail.163.com",
            "Connection": "keep-alive",
            "Referer": "https://mail.163.com/js6/main.jsp?sid="+cookie["Coremail.sid"]+"&df=mail163_letter",
            "Pragma": "no-cache",
        }
        request_data = None
        request_method = "get"
        return request_url,request_header,request_data,request_method

mylogin = DoLogin()
myrequest = MyRequester()
myparser = MyParser()
mysaver = MySaver()
mysent = MySenter(20)#设置时间间隔

def mothed(webSpider):
    webSpider.method(requester=myrequest ,parser=myparser,save=mysaver,sent=mysent,login = mylogin)
def stop(webSpider):
    webSpider.stop()
    return 1