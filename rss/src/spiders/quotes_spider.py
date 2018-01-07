# -*- coding: utf-8 -*
import scrapy

class QuotesSpider(scrapy.Spider):
	name = "quotes"

	def start_requests(self):
		urls = [
			'http://quotes.toscrape.com/page/1',
			'http://quotes.toscrape.com/page/2'
		]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		page = response.url.split('/')[-2]
		filename = 'quotes-%s.html' % page
		# print response.body.decode('utf-8').encode('gbk', 'ignore') \
		# to avoid the encode error of gbk 
		for quote in response.css('div.quote'):
			yield {
				'text': quote.css('span.text::text').extract_first(),
				'author': quote.css('small.author::text').extract_first(),
				'tag': quote.css('div.tags a.tag::text').extract()
			}
		# self.log("Save file %s" % filename)
