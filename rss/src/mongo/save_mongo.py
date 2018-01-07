# -coding: utf-8 -*-
import pymongo
from pymongo import MongoClient
# DB / COLLECTION / DOCUMENT
class DataProcess():

    def __init__(self):
        self.client = MongoClient('127.0.0.1', 27017)
        # names = client.database_names()
        # if 'db' in names:
        self.db = self.client['db']
        pass

    def create_db(self, dbname):
        if dbname == None:
            return
        if dbname not in self.client.database_names():
            db = self.client[dbname]
            db.close()

    def insert_shuimu(self, datas):
        self.client['db']['shuimu'].insert_many(datas)

    def insert_nowcoder(self, datas):
        self.client['db']['nowcoder'].insert_many(datas)
        pass

    def insert_douban(self, datas):
        self.client['db']['douban'].insert_many(datas)

    # shuimu, nowcoder, douban
    def sort_by_tag(self, tagname):
        pass

    def sort_by_time(self, days):
        pass

    def sort_by_time(self, start_time, end_time):
        pass

    def remove_old_data(self, name, time):
        pass

    def show_data(self, dbname='', collection_name=''):
        if dbname == '':
            return None
        elif collection_name == '':
            return None
        else:
            self.collection = self.db['douban']

    def show(self):
        from bson.objectid import ObjectId
        names = self.client.database_names()
        collection1 = self.db['douban']
        r = collection1.find_one({'url': 'url'})
        if collection1.find_one({'url': 'url'}):
            print 'yes', r
        else:
            print r
        collection1.delete_many({'user_id': '211'})
        collection1.delete_many({'user_id': 211})
        for c in collection1.find().sort('_id'):
            print c
        rs = collection1.find().sort('_id')
        size = 0
        for r in rs:
            size += 1
            print str(size), r['post_url']
        self.client.close()

dt = DataProcess()
dt.show()
# collection1.insert_one(
#     {
#         'user_id': '12', 'name': 'Luke'
#     }
# )

# for c in collection1.find().sort('Object_Id')[:2]:
#     print c
# collection1.drop()
# print collection1

# connection = 'shuimu'
# collection2 = db[connection]
# connection = 'douban'
# collection3 = db[connection]
# user_profiles = [
#     {'user_id': 211, 'name':'Luke'},
#     {'user_id': 212, 'name': 'Ziltoid'}
# ]
# # result = db.profiles.insert_many(user_profiles)
# res =  db.profiles.find().sort("user_id")
# for r in res:
#     print r
# print 'exist : profiles'
# print db.collection_names()


# print collection1.find({'item': 1}).count()
# client.close()
