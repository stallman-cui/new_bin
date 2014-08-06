#!/usr/bin/env python
#-*-coding:utf-8-*-
# This program is used to anlytics new created role, read data 
# from gamelog, and write some infomation to analytics.user_create_role
# 2014-07-25
# author: zwcui   cuizhw@millionhero.com

import time
import sys
reload(sys)
sys.path.append('..')
sys.setdefaultencoding('utf-8')
from models import gamelogmodel, areamodel
from models import usercreaterolemodel, userloginmodel, usernumretentionmodel

print time.ctime(), __file__, ' start...'
FORMAT = '%Y-%m-%d'
if len(sys.argv) == 1:
#    now = time.strftime(FORMAT, time.localtime())
    now = '2014-8-3'
else:
    now = sys.argv[1] 
today = time.strptime(now, FORMAT)
end = int(time.mktime(today)) - 1
start = end - 3600 * 24 + 1

glm = gamelogmodel.GameLogModel()
am = areamodel.AreaModel()
ucrm = usercreaterolemodel.UserCreateRoleModel()
ulm = userloginmodel.UserLoginModel()
unrm = usernumretentionmodel.UserNumRetentionModel()

re_time = {}
for i in range(0, 31):
    if i <= 7 or i == 14 or i == 30:
        re_time[i] = {
            'start' : start - i * 3600 * 24,
            'end' : end - i * 3600 * 24
        }
#print json.dumps(re_time, indent=2)

area = am.get_list()
user_arr = {}

for item in area:
    for plat in item['plats']:
        search = {
            'area' : str(item['_id']),
            'plat' : plat,
            'ts' : {
                '$gte' : re_time[0]['start'],
                '$lte' : re_time[0]['end']
            }
        }

        # The number of users create role and login in yesterday
        create_role_count = ucrm.get_one(search, {'_id', 'count'})
        user_login_arr = ulm.get_one(search, {'_id', 'userlist'})
        if create_role_count:
            user_total = create_role_count['count']
        else:
            user_total = 0

        fix_data = {
            'area' : str(item['_id']),
            'game' : item['game'],
            'plat' : plat,
            'ts' : start
        }
        
        __id = unrm.get_one(fix_data, {'_id'})
        fix_data['user'] = user_total

        if __id:
            mid = str(__id['_id'])
            unrm.update(mid, fix_data)
        else:
            unrm.insert(fix_data)
            
        if user_login_arr:
            login_list = user_login_arr['userlist']
        else:
            login_list = {}

        for i in range(1, 31):
            if i <= 7 or i == 14 or i == 30:
                search = {
                    'area' : str(item['_id']),
                    'plat' : plat,
                    'ts' : {
                        '$gte' : re_time[i]['start'],
                        '$lte' : re_time[i]['end']
                    }
                }
                create_role = ucrm.get_one(search, {'_id', 'userlist'})

                user_fix = {}
                if create_role:
                    role_list = create_role['userlist']
                    if len(role_list) < len(login_list):
                        user_fix = dict.fromkeys([x for x in role_list if x in login_list])
                    else: 
                        user_fix = dict.fromkeys([x for x in login_list if x in role_list ])
                
                fix_data = {
                    'game' : item['game'],
                    'area' : str(item['_id']),
                    'plat' : plat,
                    'ts' : re_time[i]['start']
                }
                __id = unrm.get_one(fix_data, {'_id'})
                fix_data[str(i) + '_retention'] = len(user_fix)
                
                if __id:
                    mid = str(__id['_id'])
                    unrm.update(mid, fix_data)
                else:
                    unrm.insert(fix_data)

print time.ctime(), __file__, ' stop...'
