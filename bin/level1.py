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
    users = gum.get_list(search, {'data.user' : 1})
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
            if not game in level_data.keys():
                level_data[game] = {}
                total_user[game] = {}
            level_data[game][area] = {
                plat : {grade : 0}
            }
            total_user[game][area] = {plat : []}
            game_info[area] = 1
        else:
            if not plat in level_data[game][area].keys():
                level_data[game][area][plat] = {grade : 0}
                total_user[game][area][plat] = []
            else:
                if not grade in level_data[game][area][plat].keys():
                    level_data[game][area][plat][grade] = 0
                    
        level_data[game][area][plat][grade] += 1
        if not acct_id in total_user[game][area][plat]:
            total_user[game][area][plat].append(acct_id)
    
data = {
    'level_data' : level_data,
    'total_user' : total_user
}    
print json.dumps(data)
