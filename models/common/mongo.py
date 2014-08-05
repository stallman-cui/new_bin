#!/usr/bin/env python
# This program is supplied the Mongodb CURD with pymongo
# 2014-07-24
# author: zwcui   cuizhw@millionhero.com

from bson.objectid import ObjectId
from pymongo import MongoClient

from config import db_config

class MongoModel:
        
    def connection(self, name):
        uri = db_config['mongo_db'][name]['uri']
        self.prefix = db_config['mongo_db'][name]['prefix']
        return MongoClient(uri)
   
    def __init__(self, name = 'default'):
        self.conn = self.connection(name)
         
    def get_db(self):
        #pass
        return 'analytics'
        
    def get_collection(self):
        #pass
        return 'gamelog'

    def insert(self, data):
        db = self.prefix + self.get_db()
        coll = self.get_collection()
        self.conn[db][coll].insert(data)

    def delete(self, id_str):
        db = self.prefix + self.get_db()
        coll = self.get_collection()
        self.conn[db][coll].remove(ObjectId(id_str))

    def update(self, id_str, change = {}):
        db = self.prefix + self.get_db()
        coll = self.get_collection()
        search = {'_id' : ObjectId(id_str)}
        return self.conn[db][coll].update(search, {'$set': change})
    
    def get_list(self, search = {}, display = {}):
        #print 'get_list: ', search, display
        db = self.prefix + self.get_db()
        coll = self.get_collection()

        if len(display):
            return self.conn[db][coll].find(search, display)
        return self.conn[db][coll].find(search)

    def get_one(self, search = {}, display = {}):
        #print 'get_one: ', search, display
        db = self.prefix + self.get_db()
        coll = self.get_collection()

        if len(display):
            return self.conn[db][coll].find_one(search, display)
        return self.conn[db][coll].find_one(search)

if __name__ == '__main__':
    test = MongoModel()
    search = {
        'op.code' : 'yuanbao_logchange',
        'ts' : {'$gte' : 1406563200, '$lte' : 1406649599}
    }

    
    fix_data ={
        'game': 'dl',
        'area': '53bdefebdbdb674228a5018b', 
        'uid': '140531009140149478', 
        'ts': 1406563200, 
        'plat': 2001
    }


    display = {
        #'_id',
        #'area',
        #'op.code',
        #'data.extra'
    }
    '''
    search_str = '53ce33bcf008b679dda5c220'
    doc = test.get_one(search_str, search = search, display = display)
    #print doc
    
    fix_data = {
        'op.code' : 'my_op.code'
    }
    test.update(search_str, search = search, change = fix_data)
    '''

    documents = test.get_list(search)


    for doc in documents:
        print doc


