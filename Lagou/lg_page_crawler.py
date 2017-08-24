#--*-coding: utf-8-*--------
import os, json, re, urllib, urllib2
from bs4 import BeautifulSoup
from lxml import etree
import html
import time
# lxml

class PageGet():
    def __init__(self):
        # This could be saved in config
        # proxies = ["http://124.88.67.63:80/","http://118.144.149.200:3128/","http://117.4.136.103:53281/","http://70.55.84.106:3128/","http://43.247.12.90:8080/","http://89.218.188.4:3128/","http://123.162.80.56:808/","http://1.179.189.217:8080/","http://198.11.137.100:80/","http://91.243.163.202:8080/","http://180.254.42.153:8080/","http://91.221.252.18:8080/","http://201.166.23.226:8080/","http://95.140.116.18:6666/","http://203.188.254.110:53281/","http://113.53.155.90:8080/","http://201.210.160.187:8080/","http://1.10.147.61:8080/","http://190.217.96.89:3128/"]

        # proxy_handler = urllib2.ProxyHandler(proxies[])
        # opener = urllib2.build_opener(proxy_handler)
        # urllib2.install_opener(opener)

        self.headers = {
            "X-Requested-With": 'XMLHttpRequest',
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36',
            "Origin": 'https://www.lagou.com',
        }
            # "Cookie": 'user_trace_token=20170211115515-2db01e4efbb24178989f2b6139d3698e; LGUID=20170211115515-e593a6c4-f00d-11e6-8f71-5254005c3644; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; index_location_city=%E5%85%A8%E5%9B%BD; login=false; unick=""; _putrc=""; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1486785316; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1486789519; _ga=GA1.2.1374329991.1486785316; LGRID=20170211130519-af0ec03c-f017-11e6-a32c-525400f775ce; TG-TRACK-CODE=search_code; JSESSIONID=A5AC6E7C54130E13C1519ABA7F70BC3C; SEARCH_ID=053c985ab53e463eb5f747658872ef29',
            # "Connection": 'keep-alive'

        self.restr = '<div class="p_top">(.*?)</div>'
        self.linkstr = '<a.*? href="(.*?)".*?>.*?<h3>(.*?)</h3>' # link, jobname
        self.filename = 'lg_links.json'
        self.pattern = re.compile(self.restr, re.S)
        self.pattern2 = re.compile(self.linkstr, re.S)
        self.jbstr = ''
        self.jobs = []
        self.ct = 0

    def start(self):
        self.urls = self.getUrls()
        self.getPage(self.urls)

    def getUrls(self):
        with open(self.filename, 'r') as f:
            raw_urls = json.load(f)
        k, urls, names = 0, [], []
        for url in raw_urls:
            jobs = url['links']
            for job in jobs:
                urls.append(job['link'])
        return urls

    def getPage(self, urls):
        for url in urls:
            self.getJobs(url)


    def getJobs(self, url):
        print("get job in", url)
        request = urllib2.Request(url, headers=self.headers)
        response = urllib2.urlopen(request).read()
        jobs = re.findall(self.pattern, response)
        if jobs == []:
            with open('lg02.log', 'a+') as f:
                f.write(repr(response).decode('string_escape') + '-' * 100 + '\n')
        print('self.ct = ', self.ct)
        print(repr(jobs).decode('string_escape'))
        for job in jobs:
            if self.ct >= 50:
                return
            self.ct += 1
            self.jobs.append(self.getJobs2(job))

    def getJobs2(self, job):
        ss = re.findall(self.pattern2, job)[0]
        print('Get ' + ss[0] + ' ' + ss[1])
        with open('data/data.txt', 'a+') as f:
            f.write('Get ' + ss[0] + ' ' + ss[1] + '\n')
        return [ss[0], ss[1]]

pg = PageGet()
time.sleep(1)
pg.start()