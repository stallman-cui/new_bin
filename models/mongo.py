#!/usr/bin/env python
# This program is supplied the Mongodb CURD with python
# 2014-07-24
# author: zwcui   cuizhw@millionhero.com

from bson import ObjectId
from pymongo import MongoClient
from config import db_config

def isset(variable):
    try:
        variable
    except:
        return 0
    else:
        return 1

class MongoModel:
        
    def connection(self, name):
        uri = db_config[name]['uri']
        self.prefix = db_config[name]['prefix']
        return MongoClient(uri)
   
    def __init__(self, name = 'default'):
        #print(db_config)
        self.conn = self.connection(name)
         
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'gamelog'


    def insert(self, data):
        db = self.prefix + self.get_db()
        coll = self.get_collection()
        self.conn[db][coll].insert(data)

    def delete(self, id_str):
        db = self.prefix + self.get_db()
        coll = self.get_collection()
        if id_str:
            self.conn[db][coll].remove(ObjectId(id_str))

    def update(self, id_str, **condition):
        db = self.prefix + self.get_db()
        coll = self.get_collection()
        if id_str:
            condition['search'] = {'_id' : ObjectId(id_str)}
        print condition
        self.conn[db][coll].update(condition['search'], {'$set' : condition['change']})

    
    def get_list(self, **condition):
        #print 'get_list: ', condition
        db = self.prefix + self.get_db()
        coll = self.get_collection()

        if 'display' in condition.keys():
            return self.conn[db][coll].find(condition['search'], condition['display'])
        else:
            return self.conn[db][coll].find(condition['search'])

    def get_one(self,  **condition):
        #print condition
        db = self.prefix + self.get_db()
        coll = self.get_collection()

        if 'id' in condition.keys():
            return self.conn[db][coll].find(condition['id'])

        if '_id' in condition.keys():
            search = {'_id' : ObjectId(condition['_id'])}
            return self.conn[db][coll].find(search)

        #print condition['search']

        if 'display' in condition.keys():
            return self.conn[db][coll].find_one(condition['search'], condition['display'])
        else:
            return self.conn[db][coll].find(condition['search'])

if __name__ == '__main__':
    test = MongoModel()
    search = {
        'ts' : {'$lt' :1402070400 , '$gt' :1401984000}
    }

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

    documents = test.get_list(search=search, display=display)
#    for doc in documents:
#        print doc
