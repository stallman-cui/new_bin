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
        pass

    def get_collection(self):
        pass

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
        db = self.prefix + self.get_db()
        coll = self.get_collection()

        if len(display):
            return self.conn[db][coll].find(search, display, timeout = False)
        return self.conn[db][coll].find(search, timeout = False)

    def get_one(self, search = {}, display = {}):
        db = self.prefix + self.get_db()
        coll = self.get_collection()

        if len(display):
            return self.conn[db][coll].find_one(search, display)
        return self.conn[db][coll].find_one(search)

    def __del__(self):
        self.conn.close()
