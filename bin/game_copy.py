#!/usr/bin/env python
#-*-coding:utf-8-*-
# This program is used to anlytics game copy from
# gamelog, and write some data to analytics.gamecopy
# and analytics.game_copy_userlist
# 2014-07-25
# author: zwcui   cuizhw@millionhero.com

import time, sys
reload(sys)
sys.path.append('..')
sys.setdefaultencoding('utf-8')

from models import gamelogmodel, areamodel
from models import gamecopymodel, gamecopyusermodel

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
gcm = gamecopymodel.GameCopyModel()
gcum = gamecopyusermodel.GameCopyUserModel()

game_info ={}
gamecopy = {}
yes_enter_user = {}
yes_pass_user = {}
search = {
    'op.code' : 'fuben_logchange',
    'ts' : {'$gte' : start, '$lte' : end}
}

data = glm.get_list(search)
for d in data:
    if d['data']['amount'] != -1:
        continue
    
    area = d['area']
    plat = d['data']['CorpId']
    acctid = d['data']['URS'].split('_')[0]
    copyid = d['data']['get_id']

    if area not in game_info.keys():
        area_info = am.get_by_idstr(area)
        if not area_info:
            continue
        game_info[area] = area_info['game']
        game = game_info[area]

        if game not in gamecopy.keys():
            gamecopy[game] = {}
            yes_enter_user[game] = {}
            yes_pass_user[game] = {}

        gamecopy[game][area] = {
            plat : {copyid : d['data']['extra']['name']}}

        yes_enter_user[game][area] = {plat : {copyid : []}}
        yes_pass_user[game][area] = {plat : {copyid : []}}
        
    else:
        game = game_info[area]
        if plat not in gamecopy[game][area].keys():
            gamecopy[game][area][plat] = {
                copyid : d['data']['extra']['name']
            }
            yes_enter_user[game][area][plat] = {copyid : []}
            yes_pass_user[game][area][plat] = {copyid : []}

        elif copyid not in gamecopy[game][area][plat].keys():
            gamecopy[game][area][plat][copyid] = d['data']['extra']['name']
            yes_enter_user[game][area][plat][copyid] = []
            yes_pass_user[game][area][plat][copyid] = []
    search = {
        'area' : area,
        'plat' : str(plat), 
        'ts' : start - 3600 * 24,
        'copyid' : copyid
    }
    
    re = gcum.get_one(search, {'enteruserlist' : 1, 'passuserlist' : 1})
    if re:
        if 'enteruserlist' in re.keys():
            yes_enter_user[game][area][plat][copyid] = re['enteruserlist']
        if 'passuserlist' in re.keys():
            yes_pass_user[game][area][plat][copyid] = re['passuserlist']

    if acctid not in yes_enter_user[game][area][plat][copyid]:
        yes_enter_user[game][area][plat][copyid].append(acctid)
    if acctid not in yes_pass_user[game][area][plat][copyid] and \
                               d['data']['extra']['iswin'] == 1:
        yes_pass_user[game][area][plat][copyid].append(acctid)

for kgame, vgame in gamecopy.items():
    for karea, varea in vgame.items():
        for kplat, vplat in varea.items():
            for kcopy, vcopy in vplat.items():
                search = {
                    'game' : kgame,
                    'area' : karea,
                    'plat' : str(kplat), 
                    'ts' : start,
                    'copyid' : kcopy
                }
                acc = {}
                fin = {}
                __id = gcum.get_one(search, {'_id'})
                try:
                    acc = yes_enter_user[kgame][karea][kplat][kcopy]
                    fin = yes_pass_user[kgame][karea][kplat][kcopy]
                except KeyError:
                    pass
                
                search['enteruserlist'] = acc
                search['passuserlist'] = fin
                
                if __id:
                    mid = str(__id['_id'])
                    gcum.update(mid, search)
                else:
                    gcum.insert(search)
                
                fix_data = {
                    'game' : kgame,
                    'plat' : str(kplat),
                    'area' : karea,
                    'ts' : start,
                    'name': vcopy,
                    'level' : kcopy
                }
                __id = gcm.get_one(fix_data, {'_id' : 1})
                fix_data['enter_user'] = len(acc)
                fix_data['pass_user'] = len(fin)

                if __id:
                    mid = str(__id['_id'])
                    gcm.update(mid, fix_data)
                else:
                    gcm.insert(fix_data)

print time.ctime(), __file__, ' stop...'
