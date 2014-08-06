#!/usr/bin/env python
#-*-coding:utf-8-*-
# This program is used to anlytics user sign up, read data from
# gamelog, and write some infomation to analytics.user_signup
# 2014-07-25
# author: zwcui   cuizhw@millionhero.com

import time, sys
reload(sys)
sys.path.append('..')
sys.setdefaultencoding('utf-8')

from models import gamelogmodel, areamodel, coindaymodel

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
cdm = coindaymodel.CoinDayModel()

game_info = {}
coin = {}
search = {
    'op.code' : 'yuanbao_logchange',
    'ts' : {'$gte' : start , '$lte' : end}
}
data = glm.get_list(search)

for d in data:
    if d['data']['amount'] > 0:
        continue
    area = d['area']
    plat = d['data']['CorpId']
    if not area in game_info.keys():
        area_info = am.get_by_idstr(area)
        game_info[area] = area_info['game']
        game = game_info[area]

        if not game in coin.keys():
            coin[game] = {}
        coin[game][area] = {
            plat : d['data']['amount']
        }
    else:
        game = game_info[area]
        if not plat in coin[game][area].keys():
            coin[game][area][plat] = d['data']['amount']
        else:
            coin[game][area][plat] += d['data']['amount']

for kgame, vgame in coin.items():
    for karea, varea in vgame.items():
        for kplat, vplat in varea.items():
             search = {
                'game' : kgame,
                'area' : karea,
                'plat' : str(kplat),
                'ts' : start
             }
             
             __id = cdm.get_one(search, {'_id', 'user'})
             search['coin'] = abs(vplat)

             if __id:
                 mid = str(__id['_id'])
                 cdm.update(mid, search)
             else:
                 cdm.insert(search)

print time.ctime(), __file__, ' stop...'
