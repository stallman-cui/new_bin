#!/usr/bin/env python
#-*-coding:utf-8-*-
# This program is used to anlytics new created role, read data 
# from gamelog, and write some infomation to analytics.user_create_role
# 2014-07-25
# author: zwcui   cuizhw@millionhero.com

import time
import json
import sys
reload(sys)
sys.path.append('..')
sys.setdefaultencoding('utf-8')

from models import areamodel, servermodel, paymentmodel
from models import usersignupmodel, userloginmodel, usercreaterolemodel

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
sm = servermodel.ServerModel()
usm = usersignupmodel.UserSignupModel()
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
        
        reg = 0
        create_role = 0
        active = 0
        
        signup_count = usm.get_one(search, {'_id', 'count'})
        if signup_count:
            reg = signup_count['count']

        create_role_count = ucrm.get_one(search, {'_id', 'count'})
        if create_role_count:
            create_role = create_role_count['count']
        
        user_login_count = ulm.get_one(search, {'_id', 'count'})
        if user_login_count:
            active = user_login_count['count']
            
        pm = paymentmodel.PaymentModel()
        search = {
            'game' : item['game'],
            'plat' : plat,
            'area' : str(item['_id']),
            'start' : start,
            'end'   : end,
            'page.index' : -1		
        }
        #print 'search: ', json.dumps(search, indent=2)
        result  = pm.get_user_payment_list(search)
        if result['status'] != 500:
            pmresult = json.loads(result['body'])
        else:
            continue

        pmresult = json.loads(result['body'])

        apru_temp = {}
        if pmresult:
            # 充值次数
            apru_temp['nodup'] = 0
            # 充值金额
            apru_temp['rmb'] = 0
            # 充值用户
            user_pay = 0
            for platdata in pmresult:
                apru_temp['nodup'] += 1
                apru_temp['rmb'] += float(platdata['rmb'])
                user_pay += 1
            # 充值用户数 
            apru_temp['count'] = user_pay
            apru = round(float(apru_temp['rmb']) / apru_temp['nodup'], 2)
        else:
            apru = "can't get data!"
            apru_temp['rmb'] = 0
            apru_temp['count'] = 0
            apru_temp['nodup'] = 0

	fix_data = {
            'area' : str(item['_id']),
            'game' : str(item['game']),
            'plat' : plat,
            'ts' : start
        }
        __id = sm.get_one(fix_data, {'_id', 'user'})
        fix_data = {
            'game' : str(item['game']),
            'area' : str(item['_id']),
            'plat' : plat,
            'ts' : start,
            'active' : active,
            'create_role' : create_role,
            'pay_amout' : apru_temp['rmb'],
            'pay_count' : apru_temp['nodup'],
            'pay_user' : apru_temp['count'],
            'reg' : reg
        }
        
        if __id:
            id = str(__id['_id'])
            sm.update(id, fix_data)
        else:
            sm.insert(fix_data)

print time.ctime(), __file__, ' stop...'
