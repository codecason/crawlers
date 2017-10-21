# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from tutorial.items import DoubanItem, DoubanPostItem

class PricePipeline(object):
    def __init__(self):
	    self.file = open('items.jl', 'wb')

    def process_item(self, item, spider):
    	if item['price']:
    		if item['price_excludes_vat']:
    			item['price'] = item['item'] * self.vat_factor
    			line = json.dumps(dict(item)) + "\n"
    			self.file.write(line)
    		return item
    	else:
    		raise DropItem('Missing price in %s' % item)


class DoubanPipeline(object):
	def __init__(self):
		port = 1000
		connection = pymongo.MongoClient("127.0.0.1", port)
		self.db = connection["douban"]
		self.douban_post = self.db["douban_post"]
	
	def process_item(self, item, spider):
		if isinstance(item, DoubanItem):
			self.saveOrUpdate(self.douban_post, item)
	
	def saveOrUpdate(self, collection, item):
		try:
			collection.insert(dict(item))
			return item
		except:
			raise DropItem("Repeat Item!")
