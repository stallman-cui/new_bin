#!/usr/bin/env python
# This program 
# 2014-07-30
# author: zwcui   cuizhw@millionhero.com

import time, hashlib
import pycurl, urllib, json, cStringIO
from common.config import db_config

### This class have a lot Repeat code with ninny.py,
### it should be alter in future
from common.config import CURL_ERROR

class PaymentModel:
    def __init__(self):
        self.__ch = pycurl.Curl()
        self.buf = cStringIO.StringIO()
        self.__ch.setopt(pycurl.WRITEFUNCTION, self.buf.write)
        self.__ch.setopt(pycurl.CONNECTTIMEOUT, 5)
        self.__ch.setopt(pycurl.FOLLOWLOCATION, True)
        self.__secret = db_config['ghoko']['secret']

    def call(self, url, query = {}, param = {}):
        #print 'param: ', json.dumps(param, indent=3)
        host = 'https://pay.millionhero.com'
        ts = str(int(time.time()))
        sign = hashlib.md5(url + ts + self.__secret ).hexdigest()
        url = '{0}{1}?ts={2}&sign={3}&{4}'.format(host, url, ts, sign, urllib.urlencode(query))

        self.__ch.setopt(pycurl.URL, url)
        self.__ch.setopt(pycurl.USERAGENT, 'MH Client')
        self.__ch.setopt(pycurl.SSL_VERIFYHOST, False)
        self.__ch.setopt(pycurl.SSL_VERIFYPEER, False)

        if len(param):
            self.__ch.setopt(pycurl.POST, True)
            self.__ch.setopt(pycurl.POSTFIELDS, json.dumps(param))
        try:
            self.__ch.perform()
            result = {
                'status' : self.__ch.getinfo(pycurl.HTTP_CODE),
                'body' : self.buf.getvalue()
            }
        except pycurl.error, e:
            errno, errstr = e
            result = {'status' : CURL_ERROR, 'body' :  errstr}
        return result

    def __del__(self):
        self.__ch.close()
        self.buf.close()

    def summary(self, plats):
        url = '/b/a'
        return self.call(url, {'plat' : plats})
        

    def count(self, interval, ts, query):
        url = '/b/b'
        params = {
            'ts' : ts,
            'interval' : interval,
            'query'	: query
        }
        return self.call(url, {}, params)


    def report(self, interval, ts, query):
        url = '/b/c'
        params = {
            'ts' : ts,
            'interval' : interval,
            'query' : query
        }
        return self.call(url, {}, params)

    def reconcile(self, game, plat, date):
        pass
	
    def get_user_total(self, data):
            url = '/b/d'
            params = {
                'user' : data['acct'],
                'game' : data['game'],
                'plat' : data['plat'],
                'area' : data['area']
            }
            return self.call(url, {}, params)

	
    def get_user_payment_list(self, data):
        url = '/b/e'
        params = {}

        if 'game' in data.keys():
            params['game'] = data['game']

        if 'plat' in data.keys():
            params['plat'] = data['plat']
                    
        if 'area' in data.keys():
            params['area'] = data['area']
            
        if 'acct' in data.keys():
            params['user'] = data['acct']

        if 'start' in data.keys():
            params['ts'] = {
                'start' :  data['start']
            }

        if 'end' in data.keys():
            params['ts']['end'] = data['end']

        if 'page.index' in data.keys():
            params['page'] = {
                'index': data['page.index']
            }

        return self.call(url, {}, params)



if __name__ == '__main__':

    url = '/b/e'
    query = {}
    param = {
        'ts' :{
            'start' : 1406822400,
            'end' : 1406908799
        },
        'page.index' : -1
    }

    ch = PaymentModel()
    result = ch.call(url, query, param)

