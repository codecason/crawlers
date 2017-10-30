# --coding: utf-8 -*-
import os, json, pymongo, datetime
class SaveTool():
	def __init__(self):
		self.connection = pymongo.MongoClient('127.0.0.1', 27017)
		self.db = self.connection['db']
		from ft.ft_tool import TimeFilter
		self.tf_tool = TimeFilter()
		self.path = os.path.dirname(__file__)

	def save_db(self, dbname, **kargs):
		date, interval = kargs['date'], kargs['interval']
		key = kargs['key']
		filename = os.path.join(self.path, 'data_' + dbname)
		ftsql = self.tf_tool.get_time_sql(interval)
		cursor = self.db[dbname].find()
		data = []
		if os.path.exists(filename) == False:
			os.mkdir(filename)
		with open(filename + '/data.jl', 'w') as f:
			f.write(repr(datetime.datetime.today()) + '\n' + '*' * 100 + '\n')
			for d in cursor:
				# d[key] = datetime.datetime.strftime(d[key], '%Y-%m-%d')
				content = d['content']
				del d['_id']
				del d['content']
				d[key] = repr(d[key])
				# print type(d['content']) : unicode
				f.write(json.dumps(d, indent=4, encoding='utf-8',ensure_ascii=False).encode('utf-8'))
				f.write('\n')
				f.write(content.encode('utf-8') + '\n')
				f.write('=' * 100 + '\n')

	def __del__(self):
		if hasattr(self, 'connection'):
			self.connection.close()

svt = SaveTool()
date = datetime.datetime.today()
dbnames = ['nowcoder', 'shuimu', 'douban']
for dbname in dbnames:
	print 'into ', dbname
	if dbname == 'douban':
		kname = 'last_time'
	else:
		kname = 'post_time'
	svt.save_db(dbname, interval=20, date=date, key=kname)
exit()