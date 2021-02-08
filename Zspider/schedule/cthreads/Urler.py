# _*_ coding: utf-8 _*_
import logging
from .base import TypeEnum, BaseThread
import multiprocessing
from .utilities import check_url_legal,get_url_legal

class Urler(BaseThread):
    """
     UrlerThread，作为BaseThread的子类
     功能：
     Url处理线程（Urler）
        a.对Process地址筛选，提取符合配置中要求格式的url地址
        b.进行去重处理（对比是否在去重集合中已经存在，存在即表示已访问过）
        c.将未访问过的url信息加入队列①待请求页面队列（request-url）
    总结：去重、加入待请求任务
    需要接收一个url，
    """
    def __init__(self, name, worker, pool):
        BaseThread.__init__(self, name, worker, pool)
        self._pool_mp = multiprocessing.Pool()
        return

    def working(self):
        # 读取待请求页面队列列表
        task_list = [self._pool.get_a_task(TypeEnum.URL_DEAL) for _ in
                     range(max(1, self._pool.get_number_dict(TypeEnum.URL_DEAL_NOT)))]
        for index in range(len(task_list)):
            for _url, _keys ,priority in filter(lambda x: check_url_legal(x[0]), task_list):
                if _keys["type"] == "index":
                    self._pool.update_number_dict(TypeEnum.URL_DEAL_SUCC, +1)
                    self._pool.add_a_task(TypeEnum.URL_REQUEST,(_url,_keys,priority))
                elif _keys["type"] == "next":
                    if (not self._worker) or self._worker.next_url_add(_url):
                        self._pool.add_a_task(TypeEnum.URL_REQUEST, (_url, _keys, priority))
                        self._pool.update_number_dict(TypeEnum.URL_DEAL_SUCC, +1)
                else:
                    if (not self._worker) or self._worker.check_and_add(_url):
                        self._pool.add_a_task(TypeEnum.URL_REQUEST, ( _url, _keys, priority))
                        self._pool.update_number_dict(TypeEnum.URL_DEAL_SUCC, +1)
                        # print(_url)
                        # print(self._worker.check_and_add(_url))
                        # print("")
                        # self._pool.update_number_dict(TypeEnum.URL_DEAL_FAIL, +1)
            self._pool.finish_a_task(TypeEnum.URL_DEAL)
        return True
