#!/usr/bin/env python
#-*-coding:utf-8-*-
# This program is used to anlytics new created role, read data 
# from gamelog, and write some infomation to analytics.user_create_role
# 2014-07-25
# author: zwcui   cuizhw@millionhero.com

import time
import sys
import json

reload(sys)
sys.path.append('..')
sys.setdefaultencoding('utf-8')
from models import gameusermodel

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

gum = gameusermodel.GameUserModel('002_h_user')

f = open('./area_plat.js', 'r')
data = json.load(f)

for v in data:

    game = v['game']
    area = v['area']
    search = {
        'area' : area
    }
    level_data = {}
    total_user = {}
    game_info = {}
    users = gum.get_list(search)
    for u in users:
        grade = u['data']['user']['Grade']
        plat_arr = u['data']['user']['URS'].split('_')
        size = len(plat_arr)
        if size > 2:
            acct_id = ''
            for i in range(0, (size -2)):
                acct_id += plat_arr[i]
        else:
            acct_id = plat_arr[0]
            
        plat = plat_arr[size -2]


        if not area in game_info.keys():    
            if not game in total_user.keys():
                total_user[game] = {}
            total_user[game][area] = {
                plat : {
                    'accts': [acct_id,],
                    grade : 0
                }
            }
            game_info[area] = 1
        else:
            if not plat in total_user[game][area].keys():
                total_user[game][area][plat] = {
                    'accts' : [acct_id,],
                    grade : 0
                }

            total_user[game][area][plat]['accts'].append(acct_id)
            total_user[game][area][plat][grade] += 1
            
    
    








'''
for d in data:
    area = d['area']
    plat = d['data']['corpid']
    if not area in game_info.keys():
        area_info = am.get_by_idstr(area)
        game_info[area] = area_info['game']
        game = game_info[area]

        if not game in create_role.keys():
            create_role[game] = {}
        
        create_role[game][area] = {
            plat : [d['data']['acct'],]
        }

    else:
        game = game_info[area]
        if not plat in create_role[game][area].keys():
            create_role[game][area][plat] = [d['data']['acct'],]
        else:
            create_role[game][area][plat].append(d['data']['acct'])

for kgame, vgame in create_role.items():
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
            __id = curm.get_one(search, {'_id', 'game'})
            search['count'] = len(user_list)
            search['userlist'] = user_list

            if __id:
                mid = str(__id['_id'])
                curm.update(mid, search)
            else:
                curm.insert(search)
'''
print time.ctime(), __file__, ' stop...'
