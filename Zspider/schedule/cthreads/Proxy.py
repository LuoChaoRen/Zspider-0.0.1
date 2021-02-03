# _*_ coding: utf-8 _*_


import logging
from .base import TypeEnum, BaseThread


class ProxiesThread(BaseThread):

    def working(self):

        proxy_state, proxy_list = self._worker.working()
        if proxy_state > 0:
            for proxy in proxy_list:
                self._pool.add_a_task(TypeEnum.PROXY, proxy)
        else:
            logging.warning("%s warning: %s", proxy_list[0], proxy_list[1])
        print(not (self._pool.get_thread_stop_flag() and self._pool.is_all_tasks_done()))
        return not (self._pool.get_thread_stop_flag() and self._pool.is_all_tasks_done())
