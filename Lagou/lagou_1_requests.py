#---*- coding:utf-8----*---
import os, urllib, re, json, requests
url = 'https://www.lagou.com/zhaopin/Java/9/?filterOption=3'
ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, \
like Gecko) Chrome/53.0.2785.89 Safari/537.36'
content = urllib.urlopen(url).read()
print(content)
