# _*_ coding: utf-8 _*_

import re
import urllib.parse
from .util_config import CONFIG_URL_LEGAL_RE, CONFIG_ERROR_MESSAGE_RE

__all__ = [
    "check_url_legal",
    "get_url_legal",
    "get_url_params",
    "get_string_num",
    "get_string_strip",
    "get_dict_buildin",
    "parse_error_message",
]


def check_url_legal(url):
    """
     正则检查url是否合法，返回True或False
    """
    return True if CONFIG_URL_LEGAL_RE.match(url) else False


def get_url_legal(url, base_url, encoding=None):

    return urllib.parse.urljoin(base_url, urllib.parse.quote(url, safe="%/:=&?~#+!$,;'@()*[]|", encoding=encoding))


def get_url_params(url, encoding="utf-8"):

    frags = urllib.parse.urlparse(url, allow_fragments=True)
    components = (frags.scheme, frags.netloc, frags.path, frags.params, "", "")
    return urllib.parse.urlunparse(components), urllib.parse.parse_qs(frags.query, encoding=encoding)


def get_string_num(string, ignore_sign=False):

    string_re = re.search(r"(?P<sign>-?)(?P<num>\d+(\.\d+)?)", string.replace(",", ""), flags=re.IGNORECASE)
    return float((string_re.group("sign") if not ignore_sign else "") + string_re.group("num")) if string_re else None


def get_string_strip(string, replace_char=" "):

    return re.sub(r"\s+", replace_char, string, flags=re.IGNORECASE).strip() if string else ""


def get_dict_buildin(dict_obj, _types=(int, float, bool, str, list, tuple, set, dict)):

    return {key: dict_obj[key] for key in dict_obj if isinstance(dict_obj[key], _types)}


def parse_error_message(line):

    r = CONFIG_ERROR_MESSAGE_RE.search(line)
    return int(r.group("priority")), eval(r.group("keys").strip()), int(r.group("deep")), r.group("url").strip()
