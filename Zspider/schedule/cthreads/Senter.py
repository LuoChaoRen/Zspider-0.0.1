# _*_ coding: utf-8 _*_

import logging
from .base import TypeEnum, BaseThread
from WorkCenter import Login
class SenterThread(BaseThread):
    def __init__(self,name,worker,pool):
        BaseThread.__init__(self, name, worker, pool)
        return
    def working(self):
        self.cookie = self._pool.get_cookie()
        sent_state,sent_res = self._worker.working(self.cookie)
        if sent_state == 200:
            logging.warning("sent: %s", sent_state)
        else:
            logging.warning("%s warning: %s", sent_res[0], sent_res[1])
        # return not (self._pool.get_thread_stop_flag() and self._pool.is_all_tasks_done())
        return not self._pool.get_stop_flg()