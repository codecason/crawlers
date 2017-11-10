# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class TutorialSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

from selenium import webdriver
from scrapy.http import HtmlResponse
import time
import requests
from scrapy.downloadermiddlewares.stats import DownloaderStats
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class ShuimuDownloaderMiddleware(object):
    cap = webdriver.DesiredCapabilities.PHANTOMJS.copy()
    item = 'phantomjs.page.customHeaders.{}'
    print 'shuimumiddle start...' * 5
    js = "var q = document.documentElement.scrollTop = 1000"
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; windows NT)'
    cap[item.format('User-Agent')] = user_agent
    cap[item.format('loadImages')] = True
    driver = webdriver.PhantomJS(desired_capabilities=cap)

    def deb(self, name):
        print ''
        print name
        print ''

    def process_request(self, request, spider):
        url = request.url
        # TO DO
        print 'meta = ', request.meta
        self.driver.get(url)
        print 'mid url = ', url
        self.deb('123456')
        # self.driver.execute_js(self.js)
        WebDriverWait(self.driver, timeout=1).until(
            EC.presence_of_element_located((By.CLASS_NAME, "bg-odd"))
        )
        # body = None? status=404?
        self.deb('1234567')
        body = self.driver.page_source
        with open('shuimu_phjs.txt', 'w') as f:
            f.write(body.encode('utf-8'))
        self.deb('12345678')
        return HtmlResponse(url=url, status=200, body=body)

    def process_response(self, response, spider):
        self.deb('123456789')
        pass
    
    def process_spider_input(self, response, spider):
        pass
    

