# -*- coding: utf-8 -*
import scrapy, re
import random
from tutorial.settings import *
from tutorial.items import DoubanPostItem
from douban_data.dirs import DOUBAN_DATAFILE

class douban_spider(scrapy.Spider):
	name = "douban"
	# allowed_domains = ["www.douban.com"]
	start_urls = [
		'https://www.douban.com/group/299259/'
	]
	hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
	{'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
	{'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]
	ct = 0
	def start_requests(self):
		for url in self.start_urls:
			yield scrapy.Request(url, callback=self.parse, headers=self.hds[0])

	def toGbk(self, s):
		s = s.strip().encode('gbk', 'ignore')
		return s

	def parse(self, response):
		# TO DO
		posts = response.css(".olt tr:not(.th)")
		# with open('log.log', 'w') as f:
		# 	f.write('wrong ' +  response.body)

		for post in posts:
			metas = {}
			if len(post.css('.pl')) != 0:
				continue
			url = post.css('.title').xpath("./a/@href").extract_first()
			title = post.css('.title').xpath("./a/text()").extract_first()

			last3 = post.xpath('./td[@nowrap]')
			author = last3[0].extract()
			metas['post_url'] = url
			metas['post_title'] = title
			metas['author'] = author

			reply_no = last3[1].xpath("./text()").extract_first(default="0")
			last_time = last3[2].xpath("./text()").extract_first("0")
			# metas['reply_no'] = reply_no
			metas['last_time'] = last_time
			print 'post_url = ', url
			print 'post_title = ', self.toGbk(title)
			print 'last_time = ', self.toGbk(last_time)
			# with open(DOUBAN_DATAFILE, 'a+') as f:
			# 	f.write(metas['post_url'] + '\n')
			yield response.follow(url, headers=self.hds[0], callback=self.parse_post, meta=metas)

	def parse_post(self, response):
		item = DoubanPostItem()
		metas = response.meta
		title = response.css('title').extract_first()
		content = ''.join(response.css('.topic-content .topic-content').xpath('./node()').extract()).strip()
		author = ''.join(response.css('.from > a::text').extract())
		# print 'author = ', self.toGbk(author)
		# print 'content = ', self.toGbk(content)
		print ''
		post_time = response.css('.color-green::text').extract_first()
		item['last_time'] = post_time
		item['post_title'] = metas['post_title']
		item['post_url'] = metas['post_url']
		item['content'] = content
		item['author'] = author
		yield item
