#!/usr/bin/env python
#-*-coding:utf-8-*-
# This program is used to anlytics new created role, read data 
# from gamelog, and write some infomation to analytics.user_create_role
# 2014-07-25
# author: zwcui   cuizhw@millionhero.com

import time, sys, json
reload(sys)
sys.path.append('..')
sys.setdefaultencoding('utf-8')
from models import userlevelmodel

print time.ctime(), __file__, ' start...'
FORMAT = '%Y-%m-%d'
if len(sys.argv) == 1:
#    now = time.strftime(FORMAT, time.localtime())
    now = '2014-8-2'
else:
    now = sys.argv[1] 
today = time.strptime(now, FORMAT)
end = int(time.mktime(today)) - 1
start = end - 3600 * 24 + 1

ulm = userlevelmodel.UserLevelModel()
data = json.loads(raw_input())

level_data = data['level_data']
print json.dumps(level_data, indent=2)
break
