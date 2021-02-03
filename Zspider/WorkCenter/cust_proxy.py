# _*_ coding: utf-8 _*_
import time

class Proxieser(object):
    def __init__(self, sleep_time=10):
        self._sleep_time = sleep_time
        return

    def working(self) -> (int, list):
        """
        :return proxies_state: -1(get failed), 1(get success)
        :return proxies_list:  [{"http(s)": "http(s)://auth@ip:port", ...], or exception[class_name, excep]
        """
        time.sleep(self._sleep_time)
        try:
            proxy_list = self.proxies_get()
            proxy_state = 1
        except Exception as excep:
            proxy_state, proxy_list = -1, [self.__class__.__name__, excep]

        return proxy_state, proxy_list

    def proxies_get(self) -> (list):
        """
           需要return proxy_list
        """
        raise NotImplementedError
