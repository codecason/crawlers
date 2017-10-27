# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from tutorial.items import *
from tutorial.utils.cleanTool import CleanTool
from tutorial.utils.gbkTool import GbkTool

# class PricePipeline(object):
#     def __init__(self):
# 	    self.file = open('items.jl', 'wb')

#     def process_item(self, item, spider):
#     	if 'price' in item:
#     		if item['price_excludes_vat']:
#     			item['price'] = item['item'] * self.vat_factor
#     			line = json.dumps(dict(item)) + "\n"
#     			self.file.write(line)
#     		return item
#     	else:
#     		raise DropItem('Missing price in %s' % item)


class DoubanPipeline(object):

	clean_tool = CleanTool()
	def open_spider(self, spider):
		if spider.name == 'douban':
			port = 27017
			try:
				self.connection = pymongo.MongoClient("127.0.0.1", port)
				self.db = self.connection["db"]
				self.douban_post = self.db['douban']
			except Exception, e:
				print e
			# self.douban_post.createIndex({"url_id":1}, {"unique":True})


	def process_item(self, item, spider):
		if isinstance(item, DoubanPostItem):
			keys = ['post_title', 'content', 'author']
			for key in keys:
				item[key] = self.clean_tool.clean(item[key])
			# print 'content = ', item['content']
			self.saveOrUpdate(self.douban_post, item)

	def saveOrUpdate(self, collection, item):
		if collection.find_one({'post_url': item['post_url']}):
			print 'item has been in the database'
			return None
		try:
			print 'insert douban' + repr(dict(item))[:100] + '...'
			collection.insert(dict(item))
			print collection.find().sort('_id')[:1]
		except:
			raise DropItem("Repeat Item!")
			print 'sorry item has problems'
			return None
		return item

class ShuimuPipeline(object):
	clean_tool = CleanTool()
	def open_spider(self, spider):
		if spider.name == 'shuimu':
			port = 27017
			print 'you have run into a spider named shuimu'
			try:
				self.connection = pymongo.MongoClient("127.0.0.1", port)
				self.db = self.connection["db"]
				self.shuimu = self.db['shuimu']
			except Exception, e:
				print e

	def process_item(self, item, spider):
		if isinstance(item, ShuimuItem):
			keys = ['post_title', 'content']
			for key in keys:
				item[key] = self.clean_tool.clean(item[key])
				# UTF-8
				print 'content = ', item['content'].decode('utf-8').encode('gbk','ignore')[:100] + '...'
			self.saveOrUpdate(self.shuimu, item)

	def saveOrUpdate(self, collection, item):
		if collection.find_one({'post_url': item['post_url']}):
			print 'data has been in {} database'.format('shuimu')
			return None
		try:
			collection.insert(dict(item))
		except:
			raise DropItem('Repeat Item Error!')
			print 'sorry has problems'
			return None
		return item

class NowcoderPipeline(object):
	clean_tool = CleanTool()
	def open_spider(self, spider):
		if spider.name == 'nowcoder':
			port = 27017
			print 'you have run into a spider named shuimu'
			try:
				self.connection = pymongo.MongoClient("127.0.0.1", port)
				self.db = self.connection["db"]
				self.post = self.db['nowcoder']
			except Exception, e:
				print e

	def process_item(self, item, spider):
		if isinstance(item, NowcoderItem):
			keys = ['post_title', 'content']
			for key in keys:
				item[key] = self.clean_tool.clean(item[key])
			self.saveOrUpdate(self.post, item)

	def saveOrUpdate(self, collection, item):
		if collection.find_one({'post_url': item['post_url']}):
			print 'data has been in {} database'.format('nowcoder')
			return None
		try:
			collection.insert(dict(item))
		except:
			raise DropItem('Repeat Item Error!')
			print 'has repeat problem'
			return None
		return item
