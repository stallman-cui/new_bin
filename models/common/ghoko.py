#!/usr/bin/env python
# This program is supplied the http search with pycurl
# 2014-07-30
# author: zwcui   cuizhw@millionhero.com

import json
from ninny import NinnyGhokoModel
from config import db_config

class GhokoModel(NinnyGhokoModel):
    __ghoko = None

    def pass_method(self, method, query, param, url = ''):
        #print 'ghokomodel: ', method, query, param, url
        if not self.__ghoko:
            self.__ghoko = NinnyGhokoModel(db_config['ghoko']['secret'])

        if not url:
            url = db_config['ghoko']['url']
        url = '{0}/{1}'.format(url.rstrip('/'), method)
        #print 'url : ', url
        data = self.__ghoko.call(url, query, param)
        if data['status'] != 200:
            raise Exception(data['body'], data['status'])
        #print 'ghoko result: ', json.loads(data['body'])
        return json.loads(data['body'])

    def dnspod(self,domain, sub):
        params = {'domain' : domain,'sub' : sub}
        return self.pass_method('dnspod', {}, params)
    
    def watchdog(self, url):
        return self.pass_method('watchdog', {'sync':'true'}, {}, url)
    
    def deliver(self, url, params):
        return self.pass_method('account-deliver', {'sync':'true'}, params, url)

    def get_account(self, url, params):
        return self.pass_method('account-get', {'sync':'true'}, params, url)
    
    def ctrl_account(self, url, params):
        return self.pass_method('account-ctrl', {'sync':'true'}, params, url)

    def sync_game_tag(self, params): 
        params['master'] = True
        return self.pass_method('game-tag-sync', {}, params)

    def init_game(self, url, params): 
        return self.pass_method('game-init', {}, params, url)
	
    def ctrl_game(self, params): 
        params['master'] = True
        return self.pass_method('game-ctrl', {}, params)

    def remove_game(self, url, area): 
        params = {'area' : area}
        return self.pass_method('game-remove', {}, params, url)

    def announce(self, params): 
        params['master'] = True
        return self.pass_method('game-announce', {}, params)
	
    def mail(self, params): 
        return self.pass_method('game-mail', {'sync':'true'}, params)

if __name__ == '__main__':
    test = GhokoModel()
    url = 'http://s28.machine.millionhero.com/ghoko'
    params = {
        'info' : {'acct' : 1},
        'account': {'id': '', 'name': ''},
        'area': '53bdefebdbdb674228a5018b',
        'plat': 2001,
        'char': {'id': '140531009140149478', 'name': ''},
        'game': 'dl',
        'port': '9009'
    }

    print test.get_account(url, params)



