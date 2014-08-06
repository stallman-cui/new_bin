#!/usr/bin/env python
#-*-coding:utf-8-*-
# This program is used to anlytics new created role, read data 
# from gamelog, and write some infomation to analytics.user_create_role
# 2014-07-25
# author: zwcui   cuizhw@millionhero.com

import time, sys
reload(sys)
sys.path.append('..')
sys.setdefaultencoding('utf-8')

from models import areamodel, regdaysmodel
from models import usersignupmodel, usercreaterolemodel

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
rdm = regdaysmodel.RegDaysModel()
usm = usersignupmodel.UserSignupModel()
ucrm = usercreaterolemodel.UserCreateRoleModel()

area = am.get_list()
for item in area:
    for plat in item['plats']:
        search = {
            'area' : str(item['_id']),
            "plat" : plat,
            'ts' : {'$gte' : start, '$lte' : end}
        }
        reg = 0
        create_role = 0
        active = 0
        
        signup_count = usm.get_one(search, {'_id', 'count'})
        if signup_count:
            reg = signup_count['count']

        create_role_count = ucrm.get_one(search, {'_id', 'count'})
        if create_role_count:
            create_role = create_role_count['count']
        
	fix_data = {
            'area' : str(item['_id']),
            'game' : str(item['game']),
            'plat' : plat,
            'ts' : start
        }
        __id = rdm.get_one(fix_data, {'_id', 'user'})
        fix_data['reg'] = reg
        fix_data['role'] = create_role
        
        if __id:
            id = str(__id['_id'])
            rdm.update(id, fix_data)
        else:
            rdm.insert(fix_data)

print time.ctime(), __file__, ' stop...'
