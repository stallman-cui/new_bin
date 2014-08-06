#!/usr/bin/env python
#-*-coding:utf-8-*-
# This program is used to anlytics new created role, read data 
# from gamelog, and write some infomation to analytics.user_create_role
# 2014-07-25
# author: zwcui   cuizhw@millionhero.com

import time, sys, json, decimal
reload(sys)
sys.path.append('..')
sys.setdefaultencoding('utf-8')

from models import areamodel, useractivitydaymodel
from models import userloginmodel, usercreaterolemodel

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

am = areamodel.AreaModel()
uadm = useractivitydaymodel.UserActivityDayModel()
ulm = userloginmodel.UserLoginModel()
ucrm = usercreaterolemodel.UserCreateRoleModel()

area = am.get_list()
user_arr = {}
for item in area:
    for plat in item['plats']:
        search = {
            'area' : str(item['_id']),
            "plat" : plat,
            'ts' : {'$gte' : start, '$lte' : end}
        }
        
        reg_total = 0
        login_total = 0

        reg_total_count = ucrm.get_one(search, {'_id', 'count'})
        if reg_total_count:
            reg_total = reg_total_count['count']
        
        user_login_count = ulm.get_one(search, {'_id', 'count'})
        if user_login_count:
            login_total = user_login_count['count']
        
	fix_data = {
            'area' : str(item['_id']),
            'game' : str(item['game']),
            'plat' : plat,
            'ts' : start
        }
        __id = uadm.get_one(fix_data, {'_id', 'user'})
        if login_total < 1:
            new_ac_rate = 0
            old_ac_rate = 0
        else:
            ## There is a elegant way use decimal module
            new_ac_rate = round(float(reg_total) / login_total * 100, 2)
            old_ac_rate = str(100 - new_ac_rate)
        fix_data = {
            'game' : str(item['game']),
            'area' : str(item['_id']),
            'plat' : plat,
            'ts' : start,
            'ac_user' : login_total,
            'new_ac_user' : reg_total,
            'new_ac_rate' : str(new_ac_rate),
            'old_ac_user' : login_total - reg_total,
            'old_ac_rate' : old_ac_rate
        }
        
        if __id:
            id = str(__id['_id'])
            uadm.update(id, fix_data)
        else:
            uadm.insert(fix_data)

print time.ctime(), __file__, ' stop...'
