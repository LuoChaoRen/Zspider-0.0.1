# _*_ coding: utf-8 _*_
import os
import json

class Login:
    def __init__(self):
        """
        1/重写登录方法获取cookie
        2/接收cookie并保存cookie
        3/如果cookie存在返回cookie
        """
        self.cookie_dir = os.path.dirname(__file__)+"/cookies.json"
        self.COOKIE = {}
        self.get_cookie_flag = 0
        return
    def working(self,pool=None):
        self._pool = pool
        if os.path.exists(self.cookie_dir) and os.path.getsize(self.cookie_dir) > 0  and self.get_cookie_flag == 0:
            with open(self.cookie_dir, "r") as cookie_f:
                cookies = cookie_f.read()
                self.COOKIE = json.loads(cookies)
            cookie_f.close()
            self._pool.updata_cookie(self.COOKIE)
        if self._pool.get_login_flag() or not os.path.exists(self.cookie_dir) or self.get_cookie_flag == 0:
            self.COOKIE =  self.get_login()
            self._pool.updata_cookie(self.COOKIE)
            self._pool.get_login_flag()
            self._pool.updata_login_flag(False)
        return not (self._pool.get_thread_stop_flag() and self._pool.is_all_tasks_done())

    def get_login(self):
        cookie_dict = self.do_login()
        COOKIE = json.dumps(cookie_dict)
        with open(self.cookie_dir,"w") as f:
            f.write(COOKIE)
        f.close()
        return cookie_dict


    def do_login(self) ->(dict):
        """
           需要return cookie_dict
        """
        raise NotImplementedError
