import logging
import multiprocessing
from .base import TypeEnum, BaseThread
from .utilities import *

class ProcesserThread(BaseThread):

    def __init__(self, name, worker, pool,spider_url,next_page_url):
        """
        功能：
        a.根据数据提取模块（cust_parser）制定的提取规则提取数据，将提取到数据格式化（save-item）
        b.存入队列③待存储队列（wait-save）
        c.将返回结果中的url信息，交给线程①url处理线程（urler）
        总结：制定提取数据，提取url,url提交到url—deal，数据提交到save
        """
        BaseThread.__init__(self, name, worker, pool)
        self._pool_mp = multiprocessing.Pool()
        self.spider_url = spider_url
        self.next_page_url = next_page_url
        self.url_parser_not = 0
        self.cookies = self._pool.get_cookie()
        return

    def working(self):
        self.url_parser_not = self._pool.get_number_dict(TypeEnum.HTM_PARSE_NOT)
        task_list = [self._pool.get_a_task(TypeEnum.HTM_PARSE) for _ in range(max(1, self.url_parser_not))]
        # task rurl, keys, rtext
        result_list = [self._pool_mp.apply_async(self._worker.working, args=(task,self.spider_url,self.next_page_url,self.cookies)) for task in task_list if task[1]["type"] != "index" or task[1]["type"] != "next"]
        for index in range(len(task_list)):
            rurl, keys, content,priority = task_list[index]
            next_set,url_set,_keys,state,item= result_list[index].get(timeout=None)
            if state>0:
                for _url in url_set:
                    self._pool.add_a_task(TypeEnum.URL_DEAL, (_url, _keys ,priority+1))
                for _nx in next_set:
                    self._pool.add_a_task(TypeEnum.URL_DEAL, (_nx, {"type":"next"}, priority + 1))
                # print("process-item:",item)
                self._pool.add_a_task(TypeEnum.ITEM_SAVE, (item, _keys ,priority))
                self._pool.update_number_dict(TypeEnum.HTM_PARSE_SUCC, +1)
                self._pool.finish_a_task(TypeEnum.HTM_PARSE)
            else:
                logging.warning("process state = 0", )
                self._pool.update_number_dict(TypeEnum.HTM_PARSE_FAIL, +1)
        return True