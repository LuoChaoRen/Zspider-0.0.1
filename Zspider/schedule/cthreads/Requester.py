import logging
import multiprocessing
from .base import TypeEnum, BaseThread
# from WorkCenter.cust_request import cust_url
from WorkCenter.cust_login import Login
class RequesterThread(BaseThread):
    def __init__(self, name, worker, pool):

        BaseThread.__init__(self, name, worker, pool)
        self._pool_mp = multiprocessing.Pool()
        self._proxy = None
        self.url_request_not = 0
        # cookie 从login获取
        return

    def working(self):
        #获取代理
        self.cookie = self._pool.get_cookie()
        if self._pool.get_proxy_flag() and (not self._proxy):
            self._proxy = self._pool.get_a_task(TypeEnum.PROXY)
        self.url_request_not = self._pool.get_number_dict(TypeEnum.URL_REQUEST_NOT)
        task_list = [self._pool.get_a_task(TypeEnum.URL_REQUEST) for _ in
                     range(max(1, self.url_request_not))]
        result_list = [self._pool_mp.apply_async(self._worker.working, args=[task,self.cookie,self._proxy]) for task in task_list]
        for index in range(len(task_list)):
            url, keys, priority = task_list[index]
            rcode, rurl, rtext, _keys  = result_list[index].get(timeout=None)
            if rcode == 200:
                self._pool.update_number_dict(TypeEnum.URL_REQUEST_SUCC, +1)
                self._pool.add_a_task(TypeEnum.HTM_PARSE, (rurl, _keys, rtext,priority))
            elif rcode == 0:
                self._pool.updata_login_flag(True)
                self._pool.add_a_task(TypeEnum.URL_REQUEST,(rurl,_keys,priority))
            else:
                self._pool.update_number_dict(TypeEnum.URL_REQUEST_FAIL, +1)
                logging.error("Request:%s error: %s", rurl, rcode)
            self._pool.finish_a_task(TypeEnum.URL_REQUEST)

        return True