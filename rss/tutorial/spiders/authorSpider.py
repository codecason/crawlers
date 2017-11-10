# -*- coding: utf-8 -*
import scrapy

class AuthorSpider(scrapy.Spider):
	name = "author"

	def start_requests(self):
		urls = [
			'http://quotes.toscrape.com',
		]
		# get cmd arguments tag: scrapy crawl author -a target=humor
		tag = getattr(self, 'tag', None)
		print '-' * 50, tag
		url = urls[0]
		if tag is not None:
			url = url + '/tag/' + tag
		yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		page = response.url.split('/')[-2]
		# print response.body.decode('utf-8').encode('gbk', 'ignore') \
		# to avoid the encode error of gbk 
		for quote in response.css('div.quote'):
			yield {
				'text': quote.css('span.text::text').extract_first(),
				'author': quote.css('small.author::text').extract_first(),
			}
		next_page = response.css('li.next a::attr(href)').extract_first()
		# linked visit
		if next_page is not None:
			yield response.follow(next_page, self.parse)
		# self.log("Save file %s" % filename)
