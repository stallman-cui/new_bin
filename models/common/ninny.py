#!/usr/bin/env python
# This program is supplied the http search with pycurl
# 2014-07-30
# author: zwcui   cuizhw@millionhero.com

import pycurl, urllib, json, cStringIO

class NinnyGhokoModel:
    def __init__(self, secret = ''):
        self._ch = pycurl.Curl()
        self.buf = cStringIO.StringIO()
        self._ch.setopt(pycurl.WRITEFUNCTION, self.buf.write)
        self._ch.setopt(pycurl.CONNECTTIMEOUT, 5)
        self._ch.setopt(pycurl.FOLLOWLOCATION, True)
        self._secret = secret

    def call(self, url, query = {}, param = {}):
        self._ch.setopt(pycurl.URL, '{0}?secret={1}&{2}'.format(url, self._secret, urllib.urlencode(query)))
        #self._ch.setopt(pycurl.URL, '{0}?{1}'.format(url, urllib.urlencode(query)))
        #print 'Request address: '
        #print 'ninny url:','{0}?secret={1}&{2}'.format(url, self._secret, urllib.urlencode(query))
        self._ch.setopt(pycurl.USERAGENT, 'GHoKo Client')
        #print 'query: ', query
        print 'param: ', json.dumps(param, indent= 3)
        if len(param):
            self._ch.setopt(pycurl.POST, True)
            self._ch.setopt(pycurl.POSTFIELDS, json.dumps(param))
        #print 'json_dumps: ', json.dumps(param)
        try:
            self._ch.perform()
            result = {
                'status' : self._ch.getinfo(pycurl.HTTP_CODE),
                'body' : self.buf.getvalue()
            }
        except pycurl.error, e:
            errno, errstr = e
            result = {'status' : 500, 'body' :  errstr}
        #print 'ninny result', result
        return result

    def __del__(self):
        self._ch.close()
        self.buf.close()

if __name__ == '__main__':
    secret = 'mhis1,000kheros'
    url = 'http://s28.machine.millionhero.com/ghoko/account-get'

    query = {
        'sync': 'true'
    }
    param = {
        'info' : {'acct' : 1},
        'account': {'id': '', 'name': ''},
        'area': '53bdefebdbdb674228a5018b',
        'plat': 2001,
        'char': {'id': '140531009140149478', 'name': ''},
        'game': 'dl',
        'port': '9009'
    }

    ch = NinnyGhokoModel(secret)
    result = ch.call(url, query, param)
    print result
