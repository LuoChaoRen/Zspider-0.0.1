# _*_ coding: utf-8 _*_

import enum
import time
import queue
import logging
import threading
import sys


class TypeEnum(enum.Enum):
    """
    TypeEnum的enum，用于标记线程池的状态
    """

    URL_DEAL = "url_deal",            # urler去重处理标志
    URL_DEAL_RUN = "url_deal_run",    # 正在urler去重处理url计数
    URL_DEAL_NOT = "url_deal_not",    # 通过urler去重处理完成的url计数
    URL_DEAL_SUCC = "url_deal_succ",  # 通过urler去重处理完成的url计数
    URL_DEAL_FAIL = "url_deal_fail",  # 通过urler去重处理完成的url计数

    URL_REQUEST = "url_request"               #url获取标志**
    URL_REQUEST_RUN = "url_request_run"        #url获取运行的标志
    URL_REQUEST_NOT = "url_request_not"        #url还没有进行提取标志
    URL_REQUEST_SUCC = "url_request_succ"       #url获取成功标志
    URL_REQUEST_FAIL = "url_request_fail"       #url获取失败标志

    HTM_PARSE = "htm_parse"               #htm解析标志**
    HTM_PARSE_RUN = "htm_parse_run"        #htm分析运行的标志
    HTM_PARSE_NOT = "htm_parse_not"        #htm parse not的标志
    HTM_PARSE_SUCC = "htm_parse_succ"       #htm解析成功标志
    HTM_PARSE_FAIL = "htm_parse_fail"       #htm解析失败标志

    ITEM_SAVE = "item_save"               #项目保存标志**
    ITEM_SAVE_RUN = "item_save_run"        #项目保存运行的标志
    ITEM_SAVE_NOT = "item_save_not"        #项目未保存标志
    ITEM_SAVE_SUCC = "item_save_succ"       #项目保存成功标志
    ITEM_SAVE_FAIL = "item_save_fail"       #项目保存失败标志

    PROXY = "proxy"                     # 代理标志
    PROXY_LIFE = "proxy_life"           # 可用的代理数
    PROXY_FAIL = "proxy_fail"           # 不可用的代理数

class BaseThread(threading.Thread):
    """
     基线程的类，作为每个线程的基类
    """

    def __init__(self, name, worker, pool):
        threading.Thread.__init__(self, name=name)
        self._worker = worker
        self._pool = pool
        self.name = name
        return

    def run(self):
        """
         重写运行函数，自动运行并且必须调用self.working()
        """
        while True:
            try:
                #如果线程的程序为false，停止执行
                if not self.working():
                    break
                if self._pool.get_stop_flg():
                    break
            #队列为空
            except queue.Empty:
                if self._pool.get_stop_flg():
                    break
                #如果get_thread_stop_flag为真，并且所有的任务都完成了（is_all_tasks_done任务都为空返回true）
                # if self._pool.get_thread_stop_flag() and self._pool.is_all_tasks_done():
                #     break
        return

    def working(self):
        """
         每个线程的程序，返回True继续，返回False停止
        """
        raise NotImplementedError


# ===============================================================================================================================
def init_monitor_thread(self, name, pool):
    """
    初始化监视线程
    """
    BaseThread.__init__(self, name, None, pool)
    self._init_time = time.time()
    self._last_request_num = 0
    self._last_parse_num = 0
    self._last_save_num = 0
    self._last_deal_url_num = 0
    return

def work_monitor(self):
    """
     监视线程池，自动运行，如果需要停止线程，则返回False
    """
    time.sleep(5)
    deal_url_run = self._pool.get_number_dict(TypeEnum.URL_DEAL_RUN)
    deal_url_not = self._pool.get_number_dict(TypeEnum.URL_DEAL_NOT)
    deal_url_succ = self._pool.get_number_dict(TypeEnum.URL_DEAL_SUCC)
    deal_url_fail = self._pool.get_number_dict(TypeEnum.URL_DEAL_FAIL)
    info = "过滤:[RUN=%d,NOT=%d,SUCC=%d,FAIL=%d];" % (
        deal_url_run,deal_url_not, deal_url_succ, deal_url_fail
    )
    request_run = self._pool.get_number_dict(TypeEnum.URL_REQUEST_RUN)
    request_not = self._pool.get_number_dict(TypeEnum.URL_REQUEST_NOT)
    request_succ = self._pool.get_number_dict(TypeEnum.URL_REQUEST_SUCC)
    request_fail = self._pool.get_number_dict(TypeEnum.URL_REQUEST_FAIL)
    info += "请求:[RUN=%d,NOT=%d,SUCC=%d,FAIL=%d];" % (
        request_run, request_not, request_succ, request_fail
    )
    parse_run = self._pool.get_number_dict(TypeEnum.HTM_PARSE_RUN)
    parse_not = self._pool.get_number_dict(TypeEnum.HTM_PARSE_NOT)
    parse_succ = self._pool.get_number_dict(TypeEnum.HTM_PARSE_SUCC)
    parse_fail = self._pool.get_number_dict(TypeEnum.HTM_PARSE_FAIL)
    info += " 提取:[RUN=%d,NOT=%d,SUCC=%d,FAIL=%d];" % (
        parse_run, parse_not, parse_succ, parse_fail
    )

    save_run = self._pool.get_number_dict(TypeEnum.ITEM_SAVE_RUN)
    save_not = self._pool.get_number_dict(TypeEnum.ITEM_SAVE_NOT)
    save_succ = self._pool.get_number_dict(TypeEnum.ITEM_SAVE_SUCC)
    save_fail = self._pool.get_number_dict(TypeEnum.ITEM_SAVE_FAIL)
    info += " 存储:[RUN=%d,NOT=%d,SUCC=%d,FAIL=%d];" % (
        save_run, save_not, save_succ, save_fail,
    )
    fh = open("temp.txt", "a+")
    sys.stdout = fh
    print(info)

    return not self._pool.get_stop_flg()
    # return not (self._pool.get_thread_stop_flag() and self._pool.is_all_tasks_done())

MonitorThread = type("MonitorThread", (BaseThread, ), dict(__init__=init_monitor_thread, working=work_monitor))

