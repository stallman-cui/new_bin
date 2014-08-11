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
    now = time.strftime(FORMAT, time.localtime())
else:
    now = sys.argv[1] 
today = time.strptime(now, FORMAT)
end = int(time.mktime(today)) - 1
start = end - 3600 * 24 + 1

ulm = userlevelmodel.UserLevelModel()
data = json.loads(raw_input())

level_data = data['level_data']
total_user = data['total_user']

if data:
    level_data = data['level_data']
    total_user = data['total_user']

    for kgame, vgame in level_data.items():
        for karea, varea in vgame.items():
            for kplat, vplat in varea.items():
                search = {
                    'area' : karea,
                    'plat' : kplat
                }

                __id = ulm.get_one(search, {'_id' : 1, 'area' : 1})
                search['game'] = kgame
                search['leveldata'] = vplat
                search['total_user'] = len(total_user[kgame][karea][kplat])
                search['ts'] = start

                if __id:
                    mid = str(__id['_id'])
                    ulm.update(mid, search)
                else:
                    ulm.insert(search)

print time.ctime(), __file__, ' stop...'
