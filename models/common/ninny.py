#!/usr/bin/env python
# This program is supplied the http search with pycurl
# 2014-07-30
# author: zwcui   cuizhw@millionhero.com

import pycurl, urllib, json, StringIO

class NinnyGhokoModel:
    def __init__(self, secret = ''):
        self._ch = pycurl.Curl()
        self.buf = StringIO.StringIO()
        self._ch.setopt(pycurl.WRITEFUNCTION, self.buf.write)
        self._ch.setopt(pycurl.CONNECTTIMEOUT, 5)
        self._ch.setopt(pycurl.FOLLOWLOCATION, True)
        self._secret = secret

    def call(self, url, query = {}, param = {}):
        self._ch.setopt(pycurl.URL, '{0}?secret={1}&{2}'.format(url, self._secret, urllib.urlencode(query)))
        #self._ch.setopt(pycurl.URL, '{0}?{1}'.format(url, urllib.urlencode(query)))
        print '{0}?{1}'.format(url, urllib.urlencode(query)), '\n\n'
        self._ch.setopt(pycurl.USERAGENT, 'GHoKo Client')
        if len(param):
            self._ch.setopt(pycurl.POST, True)
            self._ch.setopt(pycurl.POSTFIELDS, json.dumps(param))
        try:
            self._ch.perform()
            result = {
                'status' : self._ch.getinfo(pycurl.HTTP_CODE),
                'body' : self.buf.getvalue()
            }
        except pycurl.error, e:
            errno, errstr = e
            result = {'status' : 500, 'body' :  errstr}
 
        return result

    def __del__(self):
        self._ch.close()

if __name__ == '__main__':
    query = {
        'q' : 'linux'
    }
    param = {
        'name' : 'cc',
        'age' : 20
    }

    ch = NinnyGhoko()
    result = ch.call('www.baidu.com/', query, param)
    #print result
