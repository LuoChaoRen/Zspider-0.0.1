# _*_ coding: utf-8 _*_

import re
import urllib.parse
from .util_config import CONFIG_URL_LEGAL_RE

__all__ = [
    "check_url_legal",
    "get_url_legal",
]


def check_url_legal(url):
    """
     正则检查url是否合法，返回True或False
    """
    return True if CONFIG_URL_LEGAL_RE.match(url) else False


def get_url_legal(url, base_url, encoding=None):
    print("url",url)
    print("base_url",base_url)
    return urllib.parse.urljoin(base_url, urllib.parse.quote(url, safe="%/:=&?~#+!$,;'@()*[]|", encoding=encoding))



