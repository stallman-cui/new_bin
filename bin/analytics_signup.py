#!/usr/bin/env python
#-*-coding:utf-8-*-
# This program is used to anlytics user sign up, read data from
# gamelog, and write some infomation to analytics.user_signup
# 2014-07-25
# author: zwcui   cuizhw@millionhero.com

import time
import sys
reload(sys)
sys.path.append('..')
sys.setdefaultencoding('utf-8')
from models import gamelogmodel, areamodel, usersignupmodel

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

glm = gamelogmodel.GameLogModel()
am = areamodel.AreaModel()
usm = usersignupmodel.UserSignupModel()

game_info = {}
login = {}
search = {
    'op.code' : 'signup_logcount',
    'ts' : {'$gte' : start , '$lte' : end}
}
data = glm.get_list(search)

for d in data:
    area = d['area']
    plat = d['data']['corpid']
    if not area in game_info.keys():
        area_info = am.get_by_idstr(area)
        game_info[area] = area_info['game']
        game = game_info[area]

        if not game in login.keys():
            login[game] = {}
        
        login[game][area] = {
            plat : [d['data']['acct'],]
        }

    else:
        game = game_info[area]
        if not plat in login[game][area].keys():
            login[game][area][plat] = [d['data']['acct'],]
        else:
            login[game][area][plat].append(d['data']['acct'])

for kgame, vgame in login.items():
    for karea, varea in vgame.items():
        for kplat, vplat in varea.items():
            # remove the same record in the list
            user_list = list(set(vplat))
            search = {
                'game' : kgame,
                'area' : karea,
                'plat' : str(kplat),
                'ts' : start
            }
            __id = usm.get_one(search, {'_id', 'game'})
            search['count'] = len(user_list)
            search['userlist'] = user_list

            if __id:
                mid = str(__id['_id'])
                usm.update(mid, search)
            else:
                usm.insert(search)

print time.ctime(), __file__, ' stop...'
