#!/usr/bin/env python
# This program is supplied the Mongodb CURD with pymongo
# 2014-07-24
# author: zwcui   cuizhw@millionhero.com

from bson import ObjectId
from pymongo import MongoClient

from config import db_config

class MongoModel:
        
    def connection(self, name):
        uri = db_config['mongo_db'][name]['uri']
        self.prefix = db_config['mongo_db'][name]['prefix']
        return MongoClient(uri)
   
    def __init__(self, name = 'default'):
        #print(db_config)
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

        return self.conn[db][coll].find(search, display)

    def get_one(self, search = {}, display = {}):
        #print 'get_one: \n', search, display
        db = self.prefix + self.get_db()
        coll = self.get_collection()

        return self.conn[db][coll].find_one(search, display)

if __name__ == '__main__':
    test = MongoModel()
    search = {
        'ts' : {'$lt' :1402070400 , '$gt' :1401984000}
    }
    '''
    display = {
        'op.code' : 1
    }

    search_str = '53ce33bcf008b679dda5c220'
    doc = test.get_one(search_str, search = search, display = display)
    #print doc
    
    fix_data = {
        'op.code' : 'my_op.code'
    }
    test.update(search_str, search = search, change = fix_data)
    '''

    documents = test.get_list(search)

    '''
    for doc in documents:
        print doc
    '''
