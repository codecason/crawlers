# -*- coding: utf-8 -*
import scrapy, re
import random
from tutorial.settings import *
from tutorial.items import ShuimuItem
from tutorial.utils.cleanTool import CleanTool
from tutorial.utils.gbkTool import GbkTool
from douban_data.dirs import SHUIMU_DATADIR
import os


from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.xlib.pydispatch import dispatcher

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# # LOCATE WEB DRIVER => s
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import selenium.webdriver.support.ui as ui
# from selenium.webdriver.common.action_chains import ActionChains

# phpath = 'D:\\BaiduYunDownload\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe'
# cap = webdriver.DesiredCapabilities.PHANTOMJS
# cap["phantomjs.page.settings.resourceTimeout"] = 1000
# print 'initialing webdriver...'
# browser = webdriver.PhantomJS(desired_capabilities = cap)
# wait = ui.WebDriverWait(browser, 10)
# self.browser.get(url)

class ShuiMuSpider(scrapy.Spider):
    name = 'shuimu'
    start_urls = [
        # 'http://www.newsmth.net/nForum/#!mainpage'
        'http://www.newsmth.net/nForum/board/Career_Campus',
        # 'http://www.newsmth.net/nForum/board/Intern'
        # 'http://www.newsmth.net/nForum/?_escaped_fragment_=board%2FCareer_Campus',
        # 'http://www.newsmth.net/nForum/#!board/ITjob'
        # 'http://www.newsmth.net/nForum/article/Career_Campus/551303'
    ]
    header = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    item = 'phantomjs.page.customHeaders.{}'
    cap = webdriver.DesiredCapabilities.PHANTOMJS.copy()
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; windows NT)'
    cap[item.format('User-Agent')] = user_agent
    cap[item.format('loadImages')] = True

    def __init__(self):
        self.driver = webdriver.PhantomJS(desired_capabilities=self.cap)
        self.driver.set_page_load_timeout(15)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self):
        self.driver.close()

    # TO DELETE
    def __debug(self, s):
        print ''
        print s
        print ''

    def start_requests(self):
        for url in self.start_urls:
            # TO DELETE
            self.loadParse(url)
            yield scrapy.Request(url)
    
    
    ## TO DO => loadParse->parse->item
    def loadParse(self, url):
        # self.__debug('url = ' + url)
        self.driver.get(url)
        WebDriverWait(self.driver, timeout=10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'bg-odd'))
        )

        ## page.source[unicode]=>response[utf-8]=>extract[unicode]
        response = HtmlResponse(url, status=200, body = self.driver.page_source, encoding='utf-8')
        self.parse(response)

    def parse(self, response):
        # print response.body
        # with open(SHUIMU_DATADIR + '/shuimu_data.jl', 'a+') as f:
        #     # html: gb2312 -> unicode -> utf-8
        #     f.write(response.body.decode('gbk').encode('utf-8'))
        posts = response.css('tbody tr:not(.top)')
        # print 'haha ' * 100, len(posts)
        for post in posts:
            # post / td/a
            datas = post.xpath('.//td')
            url = datas[0].xpath('./a/@href').extract_first()
            title = datas[1].xpath('./a/text()').extract_first()
            post_time = datas[2].xpath('./text()').extract_first().replace('&emsp;', '')
            # print 'post_time =', post_time.encode('gbk', 'ignore')
            # post_time = datas[2].xpath('./td/text()').re('([0-9]{2}:){2}[0-9]{2}')
            metas = {"post_url": url, "post_title" : title, "post_time": post_time}
            for key in metas.keys():
                print GbkTool.toGbk(key + ' = ' + metas[key])
            yield response.follow(url, callback = self.parse_2, meta = metas)


    def parse_2(self, response):
        metas = response.meta.copy()
        self.driver.get(response.url)
        try:
            WebDriverWait(self.driver, timeout=10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'a-content'))
            )
        except Exception, e:
            print 'Error', e
        resposne = HtmlResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
        content = ''.join(response.css('.a-content').xpath('node()').extract())
        # TO DO
        tool = CleanTool()
        # if os.path.exists('./spiders/shuimu_data/') == False:
        #     os.mkdir('./spiders/shuimu_data')
        item = ShuimuItem()
        for key in metas.keys():
            item[key] = metas[key]
        item['content'] = content.encode('utf-8')
        yield item

        # with open('./spiders/shuimu_data/shuimu_data.jl', 'a+') as f:
        #     f.write('title: ' + title.encode('utf-8'))
        #     f.write(content.encode('utf-8'))
        #     f.write('=' * 50)