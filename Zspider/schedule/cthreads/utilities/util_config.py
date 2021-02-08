# _*_ coding: utf-8 _*_
import re

__all__ = [
    "CONFIG_URL_LEGAL_RE",
    "CONFIG_URL_ILLEGAL_RE",
]

# define the regex for urls
#定义URL的正则表达式 #re.IGNORECASE以不区分大小写的方式对文本做查找和替换
CONFIG_URL_LEGAL_RE = re.compile(r"^http[s]?:[^\s]+?\.[^\s]+?", flags=re.IGNORECASE)
CONFIG_URL_ILLEGAL_RE = re.compile(r"\.(cab|iso|zip|rar|tar|gz|bz2|7z|tgz|apk|exe|app|pkg|bmg|rpm|deb|dmg|jar|jad|bin|msi|"
                                   "pdf|doc|docx|xls|xlsx|ppt|pptx|txt|md|odf|odt|rtf|py|java|c|cc|js|css|log|csv|tsv|"
                                   "jpg|jpeg|png|gif|bmp|xpm|xbm|ico|drm|dxf|eps|psd|pcd|pcx|tif|tiff|"
                                   "mp3|mp4|swf|mkv|avi|flv|mov|wmv|wma|3gp|mpg|mpeg|mp4a|wav|ogg|rmvb)$", flags=re.IGNORECASE)

