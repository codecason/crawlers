# -*- coding: utf-8 -*-
import scrapy, re
from tutorial.utils import cleanTool
from tutorial.items import NowcoderItem

class NowcoderSpider(scrapy.Spider):
    name = 'nowcoder'
    start_urls = [
        # 'https://www.nowcoder.com/search?type=post&query=内推'
        'https://www.nowcoder.com/search?type=post&query=%E5%86%85%E6%8E%A8',
        # 'https://www.nowcoder.com/search?query=补招type=post&token='
        'https://www.nowcoder.com/search?query=%E8%A1%A5%E6%8B%9B&type=post&token='
    ]
    tool = cleanTool.CleanTool()
    baseurl = 'http://www.nowcoder.com'
    header = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, headers=self.header)

    def parse(self, response):
        # all posts .module-box/div.clearfix 有20+1个, 其中最后一个带有module-head, 最好删掉
        # with open('nowcoder.log', 'w') as f:
        #     f.write(response.body)
        posts = response.css('div.module-body .discuss-detail')
        for post in posts[:2]:
            url = post.css(".discuss-main").xpath('./a/@href').extract_first()
            title = post.css('.discuss-main').xpath('./a/text()').extract_first().strip()
            # <a class="d-name"> ...</a>今天 12:30<a>...</a> 抽取今天
            author = post.css('p.feed-tip a').xpath('./text()').extract_first().strip()
            post_time = post.xpath('.//p/text()').extract()[1]
            url = self.baseurl + url
            # print 'url =', url, 
            # print 'title =', title
            # print 'post_time =', repr(post_time)
            # print 'author =', author
            # print ''
            item = {}
            item['post_url'] = url; item['post_title'] = title; item['author'] = author
            item['post_time'] = post_time
            yield scrapy.Request(url, callback=self.parse_2, headers=self.header, meta=item)

    def parse_2(self, response):
        content = response.css('.post-topic-des').extract_first()
        content = self.tool.pureClean(content)
        # generate the item
        metas = response.meta
        item = NowcoderItem()
        item['author'] = metas['author']
        item['post_title'] = metas['post_title']
        item['post_url'] = metas['post_url']
        item['post_time'] = metas['post_time']
        item['content'] = content
        yield item
