# _*_ coding: utf-8 _*_
import time
import requests
from setting import request_time
import json


class Requests(object):
    def working(self,task_list:tuple,cookie:dict,proxy=None) -> (str, dict, list):
        """task_list : url, keys, priority"""
        try:
            url, keys, priority = task_list
            if keys["type"] == "index" or keys["type"] == "next":
                page_url = url
                parser_url = None
            else:
                page_url = None
                parser_url = url
            status_code,url,content = self.Request(page_url,parser_url,cookie,proxy)
            time.sleep(request_time)
            return (int(status_code),url, content, keys)
        except Exception as e:
            return (1, None, e, task_list[1])
    def Request(self,page_url,parser_url,cookie,proxy) -> (int,str,str):
        """
        :param cookie:cookie dict
        :param page_url: 起始url(start_url)或下页url(next_page_url)
        :param parser_url:
        :param proxy: 代理
        :return: int(response.status_code), response.url, response.text
        code=0时，重新登录
        """
        raise NotImplementedError
