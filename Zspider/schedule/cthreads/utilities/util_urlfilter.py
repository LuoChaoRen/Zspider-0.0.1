# _*_ coding: utf-8 _*_


from pybloom_live import ScalableBloomFilter
from .util_config import CONFIG_URL_LEGAL_RE, CONFIG_URL_ILLEGAL_RE


class UrlFilter(object):
    """
    UrlFilter类，按regex和（bloomfilter或set）筛选url
    """

    def __init__(self, black_patterns=(CONFIG_URL_ILLEGAL_RE,), white_patterns=(CONFIG_URL_LEGAL_RE,), capacity=None):
        """
        constructor, use the instance of BloomFilter if capacity else the instance of set
        构造函数，如果不是set的实例，则使用BloomFilter的实例
        """
        self._re_black_list = [item_re for item_re in black_patterns]
        self._re_white_list = [item_re for item_re in white_patterns]
        self._urlfilter = set() if not capacity else ScalableBloomFilter(capacity, error_rate=0.001)
        self._next_urlfilter = set() if not capacity else ScalableBloomFilter(capacity, error_rate=0.001)
        return

    def update(self, url_list):
        """
        使用url列表更新此url筛选器
        """
        for url in filter(lambda x: CONFIG_URL_ILLEGAL_RE.match(x), url_list):
            self._urlfilter.add(url)
        return

    def check(self, url):
        """
        检查基于self黑名单和self白名单的url
        """
        for re_black in self._re_black_list:
            if re_black.search(url):
                return False

        for re_white in self._re_white_list:
            if re_white.search(url):
                return True

        return False if self._re_white_list else True

    def check_and_add(self, url):
        """
        检查url是否不在此urlfilter中，并将url添加到此urlfilter
        """
        result = False
        if self.check(url):
            result = (url not in self._urlfilter)
            self._urlfilter.add(url)
        # print(url,self._urlfilter,result)
        return result
    def get_urlfilter(self):
        return self._re_white_list
    def next_url_add(self, url):
        result = (url not in self._next_urlfilter)
        self._next_urlfilter.add(url)
        return result