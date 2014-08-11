#!/usr/bin/env python
#-*-coding:utf-8-*-
# This program is used to anlytics shop_subyuanbao from 
# gamelog, and write some infomation to analytics.prop and prop_user_list
# 2014-07-25
# author: zwcui   cuizhw@millionhero.com

import time, sys
reload(sys)
sys.path.append('..')
sys.setdefaultencoding('utf-8')

from models import gamelogmodel, areamodel, propmodel, propusermodel

print time.ctime(), __file__, ' start...'
FORMAT = '%Y-%m-%d'
if len(sys.argv) == 1:
    now = time.strftime(FORMAT, time.localtime())
else:
    now = sys.argv[1] 
today = time.strptime(now, FORMAT)
end = int(time.mktime(today)) - 1
start = end - 3600 * 24 + 1

glm = gamelogmodel.GameLogModel()
am = areamodel.AreaModel()
pm = propmodel.PropModel()
pum = propusermodel.PropUserModel()

game_info = {}
prop = {}
search = {
    'op.code' : 'shop_subyuanbao',
    'ts' : {'$gte' : start , '$lte' : end}
}
data = glm.get_list(search)

for d in data:
    area = d['area']
    plat = d['data']['CorpId']
    acctid = d['data']['URS'].split('_')[0]
    buyitemno = d['data']['buyitemno']
    if not 'buyitemname' in d['data'].keys():
        d['data']['buyitemname'] = '无'

    if not area in game_info.keys():
        area_info = am.get_by_idstr(area)
        game_info[area] = area_info['game']
        game = game_info[area]

        if not game in prop.keys():
            prop[game] = {}
        prop[game][area] = {
            plat : {
                buyitemno : {
                    'name' : d['data']['buyitemname'],
                    'price' : d['data']['subyuanbao'] / d['data']['count'],
                    'buy_count' : 1,
                    'count' : d['data']['count'],
                    'userlist' : [acctid,]
                }
            }
        }

    else:
        game = game_info[area]
        if not plat in prop[game][area].keys():
            prop[game][area][plat] = {
                buyitemno : {
                    'name' : d['data']['buyitemname'],
                    'price' : d['data']['subyuanbao'] / d['data']['count'],
                    'buy_count' : 1,
                    'count' : d['data']['count'],
                    'userlist' : [acctid,]
                }
            }
        elif not 'buyitemno' in prop[game][area][plat].keys():
            prop[game][area][plat][buyitemno] = {
                    'name' : d['data']['buyitemname'],
                    'price' : d['data']['subyuanbao'] / d['data']['count'],
                    'buy_count' : 1,
                    'count' : d['data']['count'],
                    'userlist' : [acctid,]
            }
        else:
            prop[game][area][plat][buyitemno]['buy_count'] += 1
            prop[game][area][plat][buyitemno]['count'] += d['data']['count']
            if not acctid in prop[game][area][plat][buyitemno]['userlist']:
                prop[game][area][plat][buyitemno]['userlist'].append(acctid)
            
for kgame, vgame in prop.items():
    for karea, varea in vgame.items():
        for kplat, vplat in varea.items():
            for kitem, vitem in vplat.items():
                search = {
                    'game' : kgame,
                    'area' : karea,
                    'plat' : str(kplat),
                    'buyitemno' : kitem,
                    'ts' : start
                }
                __id = pum.get_one(search, {'_id' : 1})
                search['userlist'] = vitem['userlist']
                
                fix_data = {
                    'game' : kgame,
                    'area' : karea,
                    'plat' : str(kplat),
                    'buyitemno' : kitem,
                    'ts' : start,
                    'name' : vitem['name'],
                    'price' : vitem['price'],
                    'user_count' : len(vitem['userlist']),
                    'buy_count' : vitem['buy_count'],
                    'count' : vitem['count']
                }

                if __id:
                    mid = str(__id['_id'])
                    pum.update(mid, search)
                    pm.update(mid, fix_data)
                else:
                    pum.insert(search)
                    pm.insert(fix_data)

print time.ctime(), __file__, ' stop...'
