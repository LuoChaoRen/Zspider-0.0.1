# _*_ coding: utf-8 _*_
import time
import requests
import json

class Sent(object):
    def __init__(self,sleep_time):
        self.session = requests.session()
        self.request_method = "get"
        self.request_header = None
        self.request_data = None
        self.sleep_time = sleep_time
        return

    def working(self,cookie:dict):
        time.sleep(self.sleep_time)
        try:
            if cookie:
                for (k, v) in cookie.items():
                    self.session.cookies.set(k, v)
            request_url,request_header,request_data,request_method = self.sent_get(cookie)
            if request_header:
                self.request_header = request_header
            if request_data:
                self.request_data = request_data
            if self.request_method == "post":
                response = self.session.post(url=request_url,headers=self.request_header,data=self.request_data)
            else:
                response = self.session.get(url=request_url,headers=self.request_header)
            sent_state = response.status_code
            sent_res = response.text
        except Exception as excep:
            sent_state, sent_res = -1, [self.__class__.__name__, excep]

        return sent_state, sent_res

    def sent_get(self,cookie) -> (str,dict,dict,str):
        """
           需要return request_url,request_header,request_data,request_method
           没有传none or flase or 0
        """
        raise NotImplementedError
