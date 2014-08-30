#!/usr/bin/env python
#-*-coding:utf-8-*-
# This program is used to anlytics user login information
# from gamelog, and write some infomation to analytics.user_login_info
# 2014-07-25
# author: zwcui   cuizhw@millionhero.com

import time, sys
import pymongo
reload(sys)
sys.path.append('..')
sys.setdefaultencoding('utf-8')

from models import gamelogmodel, areamodel, userlogininfomodel

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
ulim = userlogininfomodel.UserLoginInfoModel()

game_info = {}
user = {}
search = {
    'op.code': {'$in': ['login_logcount', 'logout_logcount']},
    'ts' : {'$gte' : start , '$lte' : end}
}
data = glm.get_list(search)

for d in data:
    area = d['area']
    # so stupid, why not uniform naming?
    if d['data'].get('corpid', 0):
        plat = d['data']['corpid']
    else:
        continue

    acct = d['data']['acct']
    log_type = d['data']['type']
    if not area in game_info.keys():
        area_info = am.get_by_idstr(area)
        if not area_info:
            continue
        game_info[area] = area_info['game']
        game = game_info[area]

        if not game in user.keys():
            user[game] = {}
        
        user[game][area] = {
            plat: {
                acct: {
                    d['ts']: log_type
                }
            }
        }

    else:
        game = game_info[area]
        if not plat in user[game][area].keys():
            user[game][area][plat] = {
                acct : {
                    d['ts'] : log_type
                }
            }
        elif not acct in user[game][area][plat].keys():
            user[game][area][plat][acct] = {
                    d['ts'] : log_type
            }
        else:
            user[game][area][plat][acct][d['ts']] = log_type

for kgame, vgame in user.items():
    for karea, varea in vgame.items():
        for kplat, vplat in varea.items():
            for kacct, vacct in vplat.items():
                for ts, style in vacct.items():
                    search = {
                        'game' : kgame,
                        'area' : karea,
                        'plat' : str(kplat),
                        'acctid' : str(kacct)
                    }
                    data = ulim.get_list(search).sort('_id', pymongo.DESCENDING).limit(1)
                   
                    if data.count():
                        for i in data:
                            data = i
                    else:
                        data = {}

                    if (not data or ('login_ts' in data.keys() and data['login_ts']) \
                        and ('logout_ts' in data.keys() and data['logout_ts'])) and style == 'signin':
                        fix_data = {
                            'game' : kgame,
                            'area' : karea,
                            'plat' : str(kplat),
                            'acctid' : str(kacct),
                            'login_ts' : ts,
                            'ts' : int(time.time())
                        }
                        ulim.insert(fix_data)

                    if (not data or ('login_ts' in data and data['login_ts']) \
                        and ('logout_ts' in data and data['logout_ts'])) and style == 'signout':
                        continue
                    
                    try:
                        if data['login_ts'] and not data['logout_ts'] and style == 'signin':
                            fix_data = {'login_ts' : ts}
                            id = str(data['_id'])
                            ulim.update(id, fix_data)
                    except KeyError:
                        pass
                    
                    try:
                        if data['login_ts'] and not data['logout_ts'] and style == 'signout':
                            fix_data = {'logout_ts' : ts}
                            id = str(data['_id'])
                            ulim.update(id, fix_data)
                    except KeyError:
                        pass

print time.ctime(), __file__, ' stop...'
