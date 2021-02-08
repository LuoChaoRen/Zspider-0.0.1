import queue
import logging
import threading
from .cthreads import *
import json,sys
from schedule.cthreads.utilities import check_url_legal  #检测url是否合法


class ThreadPool(object):

    def __init__(self, parser=None, save=None, sent=None,requester=None,login=None,url_filter=None,proxy=None, queue_parse_size=-1, queue_save_size=-1, queue_proxy_size=-1):

        self._cust_parser = parser                                          #Parser解析器实例，解析器的子类或无
        self._cust_saver = save                                             #saver实例，saver的子类或无
        self._cust_request = requester                                        #url实例，requester的子类
        self._cust_proxy = proxy                                            # 代理服务器实例
        self._cust_sent = sent                                              #sent实例，senter的子类
        self._cust_login = login                                          #login实例
        self._url_filter = url_filter                                       #默认值：无，也可以是UrlFilter（） # default: None, also can be UrlFilter()

        self._thread_REQUEST_list = []                                       #获取url线程列表，在start_working（）中定义长度
        self._thread_parser = None                                          #解析器线程，如果没有解析器实例，则为None
        self._thread_saver = None                                           #saver线程，如果没有saver实例，则为None
        self._thread_senter = None                                          #senter线程，如果没有sent实例，则为None
        self._thread_requester = None                                       #requester线程
        self._thread_proxy = None                                           #proxy线程
        self._thread_stop_flag = False                                      #默认值：False，线程的停止标志 # default: False, stop flag of threads
        self._login_flag = False
        self._cookie = {}
        self._queue_deal = queue.PriorityQueue(-1)
        self._queue_url = queue.PriorityQueue(-1)
        self._queue_parse = queue.PriorityQueue(queue_parse_size)
        self._queue_save = queue.PriorityQueue(queue_save_size)
        self._queue_proxy = queue.PriorityQueue(queue_proxy_size)
        self._stop_spider = False
        self._lock = threading.Lock()                                       #_number_dict需要的锁
        self._number_dict = {

            TypeEnum.URL_DEAL_RUN:0,                                        #通过urler去重处理完成的url计数
            TypeEnum.URL_DEAL_NOT: 0,                                       # 通过urler去重处理完成的url计数
            TypeEnum.URL_DEAL_SUCC: 0,                                      # 通过urler去重处理完成的url计数
            TypeEnum.URL_DEAL_FAIL: 0,                                      # 通过urler去重处理完成的url计数

            TypeEnum.URL_REQUEST_RUN: 0,                                        #正在请求的获取任务的计数
            TypeEnum.URL_REQUEST_NOT: 0,                                        #尚未请求的URL的计数
            TypeEnum.URL_REQUEST_SUCC: 0,                                       #已成功请求的URL的计数
            TypeEnum.URL_REQUEST_FAIL: 0,                                       #请求失败的url计数

            TypeEnum.HTM_PARSE_RUN: 0,                                        #正在运行的分析任务的计数
            TypeEnum.HTM_PARSE_NOT: 0,                                        #尚未分析的URL的计数
            TypeEnum.HTM_PARSE_SUCC: 0,                                       #已成功分析的URL计数
            TypeEnum.HTM_PARSE_FAIL: 0,                                       #已分析的URL计数失败

            TypeEnum.ITEM_SAVE_RUN: 0,                                        #正在运行的保存任务的计数
            TypeEnum.ITEM_SAVE_NOT: 0,                                        #尚未保存的URL的计数
            TypeEnum.ITEM_SAVE_SUCC: 0,                                       #已成功保存的URL的计数
            TypeEnum.ITEM_SAVE_FAIL: 0,                                       #已保存的URL计数失败

            TypeEnum.PROXY_LIFE: 0,                                           # 可用的代理数
            TypeEnum.PROXY_FAIL: 0,                                           # 不可用的代理数
        }

        print("线程池已初始化")
        # logging.warning("线程池已初始化")

        self._thread_monitor = MonitorThread("monitor", self) #监视线程
        self._thread_monitor.setDaemon(True)
        self._thread_monitor.start()
        return

    def set_start_url(self, url, keys=None,priority=0):
        """
         根据“优先级”、“键”和“深度”设置起始url，重复必须为0
         执行put item 头queue fentch
        """
        self.put_item_to_queue_deal(url, keys,priority)
        return

    # 将url放入deal队列
    def put_item_to_queue_deal(self,url, keys,priority):
        """
        将url放入队列获取，键可以是字典或无
         将项目放入队列获取错误，请传递合法url

         如果正确，检测 url 合法性
         assert 为真继续执行，为假抛出异常
         URL_REQUEST，url获取标志 add_a_task条件到任务
        """
        assert check_url_legal(url), "put_item_to_queue_request error, please pass legal url"
        self.add_a_task(TypeEnum.URL_DEAL, (url, keys or {},priority))
        return
    # #response返回数据放入parser队列
    # def put_item_to_queue_parse(self, priority, url, keys, deep, content):
    #     self.add_a_task(TypeEnum.HTM_PARSE, (priority, url, keys or {}, deep, content))
    #     return
    # #将parse处理好的结果放入save队列
    # def put_item_to_queue_save(self, priority, url, keys, deep, item):
    #     self.add_a_task(TypeEnum.ITEM_SAVE, (priority, url, keys or {}, deep, item))
    #     return

    #开始工作
    def start_working(self,request_num=10,spider_url=None,next_page_url=None):
        """
         基于request_num（抓取数量）启动此线程池
        """

        print("线程池开始工作: 待处理：%s, 每次处理数量：%s", self.get_number_dict(TypeEnum.URL_DEAL_NOT), request_num)
        # logging.warning("线程池开始工作: 待处理：%s, 每次处理数量：%s", self.get_number_dict(TypeEnum.URL_DEAL_NOT), request_num)
        self._thread_stop_flag = False
        # self._stop_spider = False
        self._thread_login = self._cust_login.working(self) if self._cust_login else None
        self._thread_urler = Urler("filterurl", self._url_filter, self)
        # self._thread_requester = RequesterThread("requesturl", white_url, self,white_url_method,white_url_header,white_url_data)
        self._thread_requester_list = [RequesterThread("requesturl-%d" % (i+1), self._cust_request, self) for i in range(request_num)]
        self._thread_senter = SenterThread("senter", self._cust_sent, self) if self._cust_sent else None
        self._thread_parser = ProcesserThread("parser", self._cust_parser, self,spider_url,next_page_url) if self._cust_parser else None
        self._thread_saver = SaverThread("saver", self._cust_saver, self) if self._cust_saver else None
        self._thread_proxy = ProxiesThread("proxieser", self._cust_proxy, self) if self._cust_proxy else None
        self._thread_urler.setDaemon(True)
        self._thread_urler.start()
        # self._thread_requester.setDaemon(True)
        # self._thread_requester.start()
        for thread_requester in self._thread_requester_list:
            thread_requester.setDaemon(True)
            thread_requester.start()
        if self._thread_parser:
            self._thread_parser.setDaemon(True)
            self._thread_parser.start()

        if self._thread_saver:
            self._thread_saver.setDaemon(True)
            self._thread_saver.start()
        if self._thread_senter:
            self._thread_senter.setDaemon(True)
            self._thread_senter.start()
        if self._thread_proxy:
            self._thread_proxy.setDaemon(True)
            self._thread_proxy.start()

        print("ThreadPool starts working: success")
        # logging.warning("ThreadPool starts working: success")
        self.wait_for_finished()
        return

    def wait_for_finished(self):

        print("ThreadPool waits for finishing")
        # logging.warning("ThreadPool waits for finishing")
        self._thread_stop_flag = True

        if self._thread_urler and self._thread_urler.is_alive():
            self._thread_urler.join()
        # if self._thread_requester and self._thread_requester.is_alive():
        #     self._thread_requester.join()
        for _thread_requester in filter(lambda x: x.is_alive(), self._thread_requester_list):
            _thread_requester.join()
        if self._thread_parser and self._thread_parser.is_alive():
            self._thread_parser.join()
        if self._thread_saver and self._thread_saver.is_alive():
            self._thread_saver.join()
        if self._thread_monitor and self._thread_monitor.is_alive():
            self._thread_monitor.join()

        logging.warning("ThreadPool has finished")
        return self._number_dict

    def get_thread_stop_flag(self):
        return self._thread_stop_flag
    def get_login_flag(self):
        return self._login_flag
    def get_cookie(self):
        return self._cookie
    def updata_cookie(self,cookies):
        self._lock.acquire()
        self._cookie = cookies
        self._lock.release()
        return
    def updata_login_flag(self,upbools):
        self._lock.acquire()
        self._login_flag = upbools
        if upbools:
            self._cust_login.working(self)
        self._lock.release()
        return
    def get_proxy_flag(self):
        """
         获取此线程池的代理标志
        """
        return True if self._cust_proxy else False
    def get_number_dict(self, key=None):
        """
        如果key不为none，返回_number_dict[key]，否则返回_number_dict
        """
        return self._number_dict[key] if key else self._number_dict

    def is_all_tasks_done(self):
        return False if self._number_dict[TypeEnum.URL_DEAL_RUN] or self._number_dict[TypeEnum.URL_DEAL_NOT] or \
                        self._number_dict[TypeEnum.HTM_PARSE_RUN] or self._number_dict[TypeEnum.HTM_PARSE_NOT] or \
                        self._number_dict[TypeEnum.URL_REQUEST_RUN] or self._number_dict[TypeEnum.URL_REQUEST_NOT] or \
                        self._number_dict[TypeEnum.ITEM_SAVE_RUN] or self._number_dict[TypeEnum.ITEM_SAVE_NOT] else True

    def update_number_dict(self, key, value):
        """
         基于key更新dict值
        """
        self._lock.acquire()
        self._number_dict[key] += value
        self._lock.release()
        return

    def add_a_task(self, task_type, task):

        """
        基于任务类型添加任务
        如果类型位url标志 并且repeat大于0 --- 不是重复的url   或者  url过滤  或  url不在urlfilter里面
        put入队_queue_url
        更新字典  url还没有进行提取标志+1
        """
        if (task_type == TypeEnum.URL_DEAL):
            self._queue_deal.put(task, block=False, timeout=None)
            self.update_number_dict(TypeEnum.URL_DEAL_NOT, +1)
        elif (task_type == TypeEnum.URL_REQUEST):
            self._queue_url.put(task, block=False, timeout=None)
            self.update_number_dict(TypeEnum.URL_REQUEST_NOT, +1)
        elif (task_type == TypeEnum.HTM_PARSE) and self._thread_parser:
            self._queue_parse.put(task, block=True, timeout=None)
            self.update_number_dict(TypeEnum.HTM_PARSE_NOT, +1)
        elif (task_type == TypeEnum.ITEM_SAVE) and self._thread_saver:
            self._queue_save.put(task, block=True, timeout=None)
            self.update_number_dict(TypeEnum.ITEM_SAVE_NOT, +1)
        elif (task_type == TypeEnum.PROXY) and self._thread_proxieser:
            self._queue_proxy.put(task, block=True, timeout=None)
            self.update_number_dict(TypeEnum.PROXY_LIFE, +1)
        return


    def get_a_task(self, task_type):
        task = None
        if task_type == TypeEnum.URL_DEAL:
            task = self._queue_deal.get(block=True, timeout=5)
            self.update_number_dict(TypeEnum.URL_DEAL_NOT, -1)
            self.update_number_dict(TypeEnum.URL_DEAL_RUN, +1)
        elif task_type == TypeEnum.URL_REQUEST:
            task = self._queue_url.get(block=True, timeout=5)
            self.update_number_dict(TypeEnum.URL_REQUEST_NOT, -1)
            self.update_number_dict(TypeEnum.URL_REQUEST_RUN, +1)
        elif task_type == TypeEnum.HTM_PARSE:
            task = self._queue_parse.get(block=True, timeout=5)
            self.update_number_dict(TypeEnum.HTM_PARSE_NOT, -1)
            self.update_number_dict(TypeEnum.HTM_PARSE_RUN, +1)
        elif task_type == TypeEnum.ITEM_SAVE:
            task = self._queue_save.get(block=True, timeout=5)
            self.update_number_dict(TypeEnum.ITEM_SAVE_NOT, -1)
            self.update_number_dict(TypeEnum.ITEM_SAVE_RUN, +1)
        elif task_type == TypeEnum.PROXY:
            task = self._queue_proxy.get(block=True, timeout=5)
            self.update_number_dict(TypeEnum.PROXY_LIFE, -1)
        return task

    def finish_a_task(self, task_type):
        if task_type == TypeEnum.URL_DEAL:
            self._queue_deal.task_done()
            self.update_number_dict(TypeEnum.URL_DEAL_RUN, -1)#执行-1
        elif task_type == TypeEnum.URL_REQUEST:
            self._queue_url.task_done()
            self.update_number_dict(TypeEnum.URL_REQUEST_RUN, -1)#执行-1
        elif task_type == TypeEnum.HTM_PARSE:
            self._queue_parse.task_done()
            self.update_number_dict(TypeEnum.HTM_PARSE_RUN, -1)
        elif task_type == TypeEnum.ITEM_SAVE:
            self._queue_save.task_done()
            self.update_number_dict(TypeEnum.ITEM_SAVE_RUN, -1)
        elif task_type == TypeEnum.PROXY:
            self._queue_proxy.task_done()
        return

    def stop_spider(self):
        self._stop_spider = True
        return
    def get_stop_flg(self):
        return self._stop_spider