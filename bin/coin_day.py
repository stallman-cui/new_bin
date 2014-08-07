#!/usr/bin/env python
#-*-coding:utf-8-*-
# This program is used to anlytics user sign up, read data from
# gamelog, and write some infomation to analytics.user_signup
# 2014-07-25
# author: zwcui   cuizhw@millionhero.com

import time, sys, json
reload(sys)
sys.path.append('..')
sys.setdefaultencoding('utf-8')

from models import gamelogmodel, areamodel, coindaymodel, cointypemodel

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
ctm = cointypemodel.CoinTypeModel()

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
    coin_type = d['data']['extra']['consumetype']
    if not area in game_info.keys():
        area_info = am.get_by_idstr(area)
        game_info[area] = area_info['game']
        game = game_info[area]

        if not game in coin.keys():
            coin[game] = {}
        coin[game][area] = {
            plat : {
                coin_type : d['data']['amount']
            }
        }
    else:
        game = game_info[area]
        if not plat in coin[game][area].keys():
            coin[game][area][plat] = {
                coin_type : d['data']['amount']
            }

        else:
            if not coin_type in coin[game][area][plat].keys():
                coin[game][area][plat][coin_type] = 0
            coin[game][area][plat][coin_type] += d['data']['amount']

#print json.dumps(coin, indent=2)

for kgame, vgame in coin.items():
    for karea, varea in vgame.items():
        for kplat, vplat in varea.items():
            plat_coin = 0
            for ktype, vtype in vplat.items():
                plat_coin += vtype
                search = {
                    'game' : kgame,
                    'area' : karea,
                    'plat' : str(kplat),
                    'ts' : start,
                    'type' : ktype
                }
                __id = ctm.get_one(search, {'_id'})
                search['coin'] = abs(vtype)
                if __id:
                    mid = str(__id['_id'])
                    ctm.update(mid, search)
                else:
                    ctm.insert(search)

            search = {
                'game' : kgame,
                'area' : karea,
                'plat' : str(kplat),
                'ts' : start,
            }
            __id = cdm.get_one(search, {'_id'})
            search['coin'] = abs(plat_coin)
            if __id:
                mid = str(__id['_id'])
                cdm.update(mid, search)
            else:
                cdm.insert(search)

print time.ctime(), __file__, ' stop...'
