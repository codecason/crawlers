# =*= coding: utf-8 -*-

from ft_tool import TimeFilter
import pymongo
from pymongo import MongoClient
import datetime
tft = TimeFilter()
tsql = tft.get_sql_dict(7)
port = 27017
connection = pymongo.MongoClient("127.0.0.1", port)
db = connection["db"]
def run():
    global db, connection
    try:
        post = db['douban']
        tsql = {'$lt': '2017-09-20 18:29:27'}
        res = post.find({'last_time': tsql})
        res = post.find().sort('last_time')
        default = False
        db.douban.insert({"post_time": 'haha'})
        if default == False:
            while 1:
                x = raw_input('dbname:')
                post = db[x]
                key = raw_input('key name:')
                res = post.find().sort(key)
                t = raw_input('range:')

                ed = None if t == '0' else int(t)
                for r in res:
                    print repr(r)[:100]
                    if key != '0':
                        print repr(r[key])[:ed]
                    else:
                        print repr(r)[:ed]
        else:
            while 1:
                x = raw_input('dbname:')
                post = db[x]
                res = post.find()
                print 'res = '
                for r in res:
                    print r
    finally:
        connection.close()

def run2():
    global connection
    try:
    finally:
        connection.close()
    pass
run2()
        # post.insert({'last_time': datetime.datetime.today()})
        # post.insert({'last_time': datetime})
        # RES = post.remove({'last_time': '2017-09-20 18:29:27'})