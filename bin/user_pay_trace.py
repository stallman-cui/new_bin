#!/usr/bin/env python
#-*-coding:utf-8-*-
# This program is used to anlytics new created role, read data 
# from gamelog, and write some infomation to analytics.user_create_role
# 2014-07-25
# author: zwcui   cuizhw@millionhero.com

import time, sys, json
reload(sys)
sys.path.append('..')
sys.setdefaultencoding('utf-8')

from models import areamodel, paymentmodel
from models import usercreaterolemodel, userpaytracemodel

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
ucrm = usercreaterolemodel.UserCreateRoleModel()
uptm = userpaytracemodel.UserPayTraceModel()
pm = paymentmodel.PaymentModel()

pay_time = {}
for i in range(0, 31):
    if i <= 6 or i == 13 or i == 29:
        pay_time[i] = {
            'start' : start - i * 3600 * 24,
            'end' : end - i * 3600 * 24
        }
#print json.dumps(pay_time, indent=2)
search = {
    'start' : pay_time[0]['start'],
    'end' : pay_time[0]['end'],
    'page.index' : -1
}
result  = pm.get_user_payment_list(search)
pmresult = json.loads(result['body'])
user_pay_list = {}
create_role_list = {}
game_info = {}

for pmv in pmresult:
    game = pmv['game']
    area = pmv['area']
    plat = pmv['plat']

    if not area in game_info.keys():
        if not game in user_pay_list.keys():
            user_pay_list[game] = {}
        user_pay_list[game][area] = {
            plat : [pmv['user'], ]
        }
        game_info[area] = 1

    elif not plat in user_pay_list[game][area].keys():
        user_pay_list[game][area][plat] = [pmv['user'], ]
    else:
        if pmv['user'] not in user_pay_list[game][area][plat]:
            user_pay_list[game][area][plat].append(pmv['user'])
    
search = {
    'ts' : {
        '$in' : [
            pay_time[0]['start'],
            pay_time[1]['start'],
            pay_time[2]['start'],
            pay_time[3]['start'],
            pay_time[4]['start'],
            pay_time[5]['start'],
            pay_time[6]['start'],
            pay_time[13]['start'],
            pay_time[29]['start']
        ]
    }
}

create_role_data = ucrm.get_list(search)
for role in create_role_data:
    game = role['game']
    area = role['area']
    plat = role['plat']
    ts = role['ts']
    
    if not ts in create_role_list.keys():
        create_role_list[ts] = {game : {area : {plat : role['userlist']}}}

    if game not in create_role_list[ts].keys():
        create_role_list[ts][game] = {area : {plat : role['userlist']}}

    elif area not in create_role_list[ts][game].keys():
        create_role_list[ts][game][area] = {plat : role['userlist']}

    elif plat not in create_role_list[ts][game][area].keys():
        create_role_list[ts][game][area][plat] = role['userlist']


area = am.get_list()
for item in area:
    for plat in item['plats']:
        game = item['game']
        area = str(item['_id'])
        fix_data = {
            'area' : area,
            'game' : game,
            'plat' : plat,
            'ts' : pay_time[0]['start']
        }

        __id = uptm.get_one(fix_data, {'_id'})
        ts = pay_time[0]['start']
        fix_data['create_role_count'] = 0
        fix_data['pay_user_count'] = 0
        try:
           fix_data['create_role_count'] = len(create_role_list[ts][game][area][plat])
        except KeyError:
           pass
        try:
            user_fix = dict.fromkeys([x for x in create_role_list if x in user_pay_list])
            fix_data['pay_user_count'] = len(user_fix)
        except KeyError:
            pass
        
        if __id:
            id = str(__id['_id'])
            uptm.update(id, fix_data)
        else:
            uptm.insert(fix_data)
        
        for i in range(1, 31):
            if i <= 6 or i == 13 or i == 29:
                ts = pay_time[i]['start']
                pay_user = {}
                
                try:
                    pay_user = user_pay_list[game][area][plat]
                except KeyError:
                    pass

                create_role_user = {}
                try:
                    create_role_user = create_role_list[ts][game][area][plat]
                except KeyError:
                    pass
                if len(create_role_user) and len(pay_user):
                    user_fix = dict.fromkeys([x for x in create_role_user, pay_user])
                
                fix_data = {
                    'area' : str(item['_id']),
                    'game' : game,
                    'plat' : plat,
                    'ts' : pay_time[i]['start']
                }
                __id = uptm.get_one(fix_data, {'_id'})
                fix_data[str(i) + '_retention'] = len(user_fix)
                if __id:
                    id = str(__id['_id'])
                    uptm.update(id, fix_data)
                else:
                    uptm.insert(fix_data)

print time.ctime(), __file__, ' stop...'
