#!/usr/bin/env python
# This program 
# 2014-07-30
# author: zwcui   cuizhw@millionhero.com

from common.mongo import MongoModel 
from accountlistmodel import AccountListModel

class AccountUserModel(MongoModel, object):
    def get_db(self):
        return 'mhgame'

    def get_collection(self):
        return 'user'

    def get_one(self, search = {}):
        params = {
            "area" : search["area"],
            "data.user.CorpId" : int(search["plat"]),
            "data.user.Uid" : search["uid"]
        }       
        user = super(AccountUserModel, self).get_one(params)
        
        id = user["data"]["user"]["URS"];
        alm =  AccountListModel("002_h_user");
        params = {'data.URS' : id}
        list = alm.get_one(params)
        result = {
            "rest_yuanbao" : list["data"]["YuanBao"],
            "birthday" : user["data"]["user"]["Birthday"],
            "recent_login" : user["data"]["user"]["LoginTime"],
        }
            
        return result;         
