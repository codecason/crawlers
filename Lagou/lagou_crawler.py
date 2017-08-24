#---*- coding:utf-8----*---
import os, urllib, urllib2, re, json
import lg_page_crawler as lgp

class Lagou():
    def __init__(self):
        self.url = "http://www.lagou.com"
        self.restr = "<dd>(.*?)</dd>"
        self.filename = "lg_links.txt"
        self.addHeaders()
    def start(self):
        self.pattern = re.compile(self.restr, re.S)
        self.getpage()
        self.getJobInfo(self.jobs)
        self.saveJob()
    def addHeaders(self):
        print 'in add headers'
        self.headers = {
            "X-Requested-With": 'XMLHttpRequest',
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36',
            "Origin": 'https://www.lagou.com',
            "Cookie": 'user_trace_token=20170211115515-2db01e4efbb24178989f2b6139d3698e; LGUID=20170211115515-e593a6c4-f00d-11e6-8f71-5254005c3644; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; index_location_city=%E5%85%A8%E5%9B%BD; login=false; unick=""; _putrc=""; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1486785316; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1486789519; _ga=GA1.2.1374329991.1486785316; LGRID=20170211130519-af0ec03c-f017-11e6-a32c-525400f775ce; TG-TRACK-CODE=search_code; JSESSIONID=A5AC6E7C54130E13C1519ABA7F70BC3C; SEARCH_ID=053c985ab53e463eb5f747658872ef29',
            "Connection": 'keep-alive'
        }
    def getpage(self):
        print 'in get page'
        request = urllib2.Request(self.url, headers=self.headers)
        response = urllib2.urlopen(request).read()
        print type(response)
        print 'in get page'
        allfound = re.findall(self.pattern, response)
        print(repr(allfound))
        j = 0
        #先得到所有的dd项目再找到各个项目里的a链接
        pattern_of_get_link = re.compile("<a href=\"(.*?)\".*?>(.*?)</a>", re.S)
        print 'in get page'
        jobs = []
        j = 0
        for i in allfound:
            j += 1
            if j >= 7:
                break # 拉勾APP 移动开发 前端开发 测试 运维 DBA
            links = self.get_all_link(pattern_of_get_link, i)
            job = {"links":links, "field":""}
            jobs.append(job)
        print 'in get page'
        self.jobs = jobs
        # newtool = Tool()
        # newtool.json_print(jobs)
        print 'in get page'
        return self.jobs

    def getJobInfo(self, jobs):
        print 'in get job info'
        for i in jobs:
            item = dict()
            item = i
            field = item['field']
            print field
            links = item['links']
            for j in links:
                link = j['link']
                print link
        print 'in get job info'

    def get_all_link(self, pattern, pagestr):
        links = []
        findstr = re.findall(pattern, pagestr)
        for i in findstr:
            links.append({"link":i[0], "jobname":i[1]})
        return links

    def saveJob(self):
        print 'in save job'
        with open(self.filename, 'w') as f:
            ss = json.dumps(self.jobs, ensure_ascii=False)
            f.write(ss)
        print 'in save job'

lg = Lagou()
# lg.start()
g = lgp.PageGet()


import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time

chromedriver = 'C:\\Users\\hugo\\AppData\\Local\\Google\\Chrome\\Application\\chromedriver.exe'
os.environ['webdriver.chrome.driver'] = chromedriver

def getJobItem(joburl):
    headers = {
        "X-Requested-With": 'XMLHttpRequest',
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36',
        "Origin": 'https://www.lagou.com',
        "Cookie": 'user_trace_token=20170211115515-2db01e4efbb24178989f2b6139d3698e; LGUID=20170211115515-e593a6c4-f00d-11e6-8f71-5254005c3644; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; index_location_city=%E5%85%A8%E5%9B%BD; login=false; unick=""; _putrc=""; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1486785316; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1486789519; _ga=GA1.2.1374329991.1486785316; LGRID=20170211130519-af0ec03c-f017-11e6-a32c-525400f775ce; TG-TRACK-CODE=search_code; JSESSIONID=A5AC6E7C54130E13C1519ABA7F70BC3C; SEARCH_ID=053c985ab53e463eb5f747658872ef29',
        "Connection": 'keep-alive'
    }
    driver = webdriver.Chrome(chromedriver)
    driver.get(joburl)
    cookie = driver.get_cookies()
    print repr(cookie).decode('string_escape')
    job = {'position':'', 'money':'', 'company_name':'', }
    pass

# job = 'https://www.lagou.com/jobs/list_%E5%AE%9E%E4%B9%A0?px=default&city=%E5%85%A8%E5%9B%BD#filterBox'
# getJobItem(job)
# 拉勾APP
# //www.lagou.com/zhaopin/Java/
# //www.lagou.com/zhaopin/Python/
# //www.lagou.com/zhaopin/PHP/
# //www.lagou.com/zhaopin/.NET/
# //www.lagou.com/zhaopin/C%23/
# //www.lagou.com/zhaopin/C%2B%2B/
# //www.lagou.com/zhaopin/C/
# //www.lagou.com/zhaopin/VB/
# //www.lagou.com/zhaopin/Delphi/
# //www.lagou.com/zhaopin/Perl/
# //www.lagou.com/zhaopin/Ruby/
# //www.lagou.com/zhaopin/Hadoop/
# //www.lagou.com/zhaopin/Node.js/
# //www.lagou.com/zhaopin/shujuwajue/
# //www.lagou.com/zhaopin/ziranyuyanchuli/
# //www.lagou.com/zhaopin/sousuosuanfa/
# //www.lagou.com/zhaopin/jingzhuntuijian/
# //www.lagou.com/zhaopin/quanzhangongchengshi/
# //www.lagou.com/zhaopin/go/
# //www.lagou.com/zhaopin/asp/
# //www.lagou.com/zhaopin/shell/
# //www.lagou.com/zhaopin/houduankaifaqita/
# 移动开发
# //www.lagou.com/zhaopin/HTML5/
# //www.lagou.com/zhaopin/Android/
# //www.lagou.com/zhaopin/iOS/
# //www.lagou.com/zhaopin/WP/
# //www.lagou.com/zhaopin/yidongkaifaqita/
# 前端开发
# //www.lagou.com/zhaopin/webqianduan/
# //www.lagou.com/zhaopin/Flash/
# //www.lagou.com/zhaopin/html51/
# //www.lagou.com/zhaopin/JavaScript/
# //www.lagou.com/zhaopin/U3D/
# //www.lagou.com/zhaopin/COCOS2D-X/
# //www.lagou.com/zhaopin/qianduankaifaqita/
# 测试
# //www.lagou.com/zhaopin/ceshigongchengshi/
# //www.lagou.com/zhaopin/zidonghuaceshi/
# //www.lagou.com/zhaopin/gongnengceshi/
# //www.lagou.com/zhaopin/xingnengceshi/
# //www.lagou.com/zhaopin/ceshikaifa/
# //www.lagou.com/zhaopin/youxiceshi/
# //www.lagou.com/zhaopin/baiheceshi/
# //www.lagou.com/zhaopin/huiheceshi/
# //www.lagou.com/zhaopin/heiheceshi/
# //www.lagou.com/zhaopin/shoujiceshi/
# //www.lagou.com/zhaopin/yingjianceshi/
# //www.lagou.com/zhaopin/ceshijingli2/
# //www.lagou.com/zhaopin/ceshiqita/
# 运维
# //www.lagou.com/zhaopin/yunweigongchengshi/
# //www.lagou.com/zhaopin/yunweikaifagongchengshi/
# //www.lagou.com/zhaopin/wangluogongchengshi/
# //www.lagou.com/zhaopin/xitonggongchengshi/
# //www.lagou.com/zhaopin/ITzhichi/
# //www.lagou.com/zhaopin/idc/
# //www.lagou.com/zhaopin/cdn/
# //www.lagou.com/zhaopin/f5/
# //www.lagou.com/zhaopin/xitongguanliyuan/
# //www.lagou.com/zhaopin/bingdufenxi/
# //www.lagou.com/zhaopin/webanquan/
# //www.lagou.com/zhaopin/wangluoanquan/
# //www.lagou.com/zhaopin/xitonganquan/
# //www.lagou.com/zhaopin/yunweijingli/
# //www.lagou.com/zhaopin/yunweiqita/
# DBA
# //www.lagou.com/zhaopin/MySQL/
# //www.lagou.com/zhaopin/SQLServer/
# //www.lagou.com/zhaopin/Oracle/
# //www.lagou.com/zhaopin/DB2/
# //www.lagou.com/zhaopin/MongoDB/
# //www.lagou.com/zhaopin/etl/
# //www.lagou.com/zhaopin/hive/
# //www.lagou.com/zhaopin/shujucangku/
# //www.lagou.com/zhaopin/dbaqita/