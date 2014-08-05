#!/usr/bin/env python
# This program 
# 2014-07-30
# author: zwcui   cuizhw@millionhero.com

from bson.objectid import ObjectId

from common.mongo import MongoModel 
from common.ghoko import GhokoModel
from areamodel import AreaModel
from hostmodel import HostModel

class AccountModel(MongoModel, object):
    def get_db(self):
        return 'game'

    def get_collection(self):
        return 'account'

    def get_one(self, search = {}):
        data = super(AccountModel, self).get_one(search)

        if not data:
            s = {
                '_id' :  ObjectId(search['area_id'])
            }
            area = AreaModel().get_one(s)
            if not area:
                return 

            host = HostModel().get_one(search = {'id' : area['host']})
            if not host:
                return 
                
            if not search.get('info', 0):
                search['info'] = ''

            params = {
                'port'	: area['port']['mcs'],
                'game'	: search['game_tag'],
                'plat'	: search['plat_id'],
                'area'	: search['area_id'],
                'account' : search['account'],
                'char' : search['char'],
                'info' : search['info']
            }
            
            acct = GhokoModel().get_account(host['ghoko'], params)
            if not acct or type(acct) == type(1):
                return False

            id = ''
            if acct.get('acct_id', 0):
                id = acct['acct_id']

            name = ''
            if acct.get('acct', 0):
                name = acct['acct']

            data = {
                'game_tag' : search['game_tag'],
                'plat_id' : search['plat_id'],
                'area_id' : search['area_id'],
                'account' : {
                    'id' : id,
                    'name' : name
                    }
            }
            
            for k, v in acct['char_msg'].items():
                temp = {'id' : k}
                for k1, v1 in v.items():
                    temp[k1] = v1
                data['char'] = temp

            self.insert(data)
            return data

    def ctrl(search, data):
        s = {
            'game' : search['game_tag'],
            'plats'	: search['plat_id'],
            '_id' : ObjectId(search['area_id']),
        }

        area= AreaModel().get_one(s)
        if not area:
            raise Exception("Area({s['id']}) not found!");

        host = HostModel().get_one({'id' : area['host']})
        if not host:
            raise Exception("Host({area['host']}) not found!");

        data['port'] = area['port']['mcs'];
        return GhokoModel.ctrl_account(host['ghoko'], data);

if __name__ == '__main__':
    test = AccountModel()

    search = {
        'info': {'acct': 1},
        'account': {'id': '', 'name': ''}, 
        'area_id': u'53bdefebdbdb674228a5018b', 
        'char': {'id': u'140531009140149478', 'name': ''}, 
        'game_tag': u'dl', 
        'plat_id': 2001
    }
    
    doc = test.get_one(search)
    print doc
