# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from tutorial.items import *
from tutorial.utils.cleanTool import CleanTool
from tutorial.utils.gbkTool import GbkTool
import datetime

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

	def process_item(self, item, spider):
		if isinstance(item, DoubanPostItem):
			if self.douban_post.find_one({'post_url': item['post_url']}):
				print 'item has been in the database'
				return None
			# TO DELETE
			# print '1' * 200
			keys = ['post_title', 'content', 'author']
			for key in keys:
				item[key] = self.clean_tool.clean(item[key])

			# format: 10-20 20:30 or 2016-10-20
			last_time = item['last_time']
			if len(last_time) == 11:
				year = datetime.datetime.today().year
				last_time = datetime.datetime.strptime(str(year) + '-' + last_time, '%Y-%m-%d')
			elif len(last_time) == 10:
				last_time = datetime.datetime.strptime(last_time, '%Y-%m-%d')
			item['last_time'] = last_time
			print last_time
			# print 'content = ', item['content']
			self.saveOrUpdate(self.douban_post, item)
		return item

	def saveOrUpdate(self, collection, item):
		# if collection.find_one({'post_url': item['post_url']}):
		# 	print 'item has been in the database'
		# 	return None
		try:
			print 'insert douban' + repr(dict(item))[:100] + '...'
			collection.insert(dict(item))
			# TO DELETE
			# print collection.find().sort('_id')[:1]
		except:
			raise DropItem("Repeat Item!")
			print 'sorry item has problems'
			return None
		return item

	def queryItem(self, days):
		item = ['query']
		between = self.timefilter.sql_filter('week')
		results = self.douban_post.find({"time": between})
		for res in results:
			print res
	
	def close_spider(self, spider):
		if hasattr(self, 'connection'):
			self.connection.close()

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
			# TO DELETE
			# print '2' * 200
			if self.shuimu.find_one({'post_url': item['post_url']}):
				print 'data has been in {} database'.format('shuimu')
				return None
			keys = ['post_title', 'content']
			for key in keys:
				item[key] = self.clean_tool.clean(item[key])
				# UTF-8
			post_time = item['post_time'].strip()
			if len(post_time) == 5:
				post_time = datetime.datetime.today().year + '-' + post_time
			elif post_time.find(':') != -1:
				post_time = datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')
			item['post_time'] = datetime.datetime.strptime(post_time, '%Y-%m-%d')
			# print 'post_time = ', repr(item['post_time'])
			self.saveOrUpdate(self.shuimu, item)
		return item

	def saveOrUpdate(self, collection, item):
		# if collection.find_one({'post_url': item['post_url']}):
		# 	print 'data has been in {} database'.format('shuimu')
		# 	return None
		# print 'content = ', item['content'].decode('utf-8').encode('gbk','ignore')[:100] + '...'
		try:
			collection.insert(dict(item))
		except:
			raise DropItem('Repeat Item Error!')
			print 'sorry has problems'
			return None
		return item

	def close_spider(self, spider):
		if hasattr(self, 'connection'):
			self.connection.close()


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
			if self.post.find_one({'post_url': item['post_url']}):
				print 'data has been in {} database'.format('nowcoder')
				return None
			# TO DELETE
			# print '3' * 200
			keys = ['post_title', 'content']
			for key in keys:
				item[key] = self.clean_tool.clean(item[key])
			post_time = item['post_time']
			if post_time.find(':') != -1:
				post_time = TimeFilter.get_today_str()
			item['post_time'] = datetime.datetime.strptime(post_time, '%Y-%m-%d')
			self.saveOrUpdate(self.post, item)
			# print 'content = ', item['content'].encode('gbk', 'ignore')[:100]
			# print 'post_time = ', item['post_time'].encode('gbk', 'ignore')
		return item

	def saveOrUpdate(self, collection, item):
		# if collection.find_one({'post_url': item['post_url']}):
		# 	print 'data has been in {} database'.format('nowcoder')
		# 	return None
		try:
			collection.insert(dict(item))
		except:
			raise DropItem('Repeat Item Error!')
			print 'has repeat problem'
			return None
		return item

	def close_spider(self, spider):
		if hasattr(self, 'connection'):
			self.connection.close()
