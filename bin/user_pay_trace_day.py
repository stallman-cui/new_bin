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

from models import areamodel, payorderuserlistmodel, paymentmodel
from models import usercreaterolemodel, userpaytracemodel, userpaytracedaymodel

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
uptdm = userpaytracedaymodel.UserPayTraceDayModel()
poulm = payorderuserlistmodel.PayOrderUserListModel()
pm = paymentmodel.PaymentModel()

search = {
    'start' : start,
    'end' : end,
    'page.index' : -1
}
result  = pm.get_user_payment_list(search)
pmresult = json.loads(result['body'])
user_pay_list = {}
user_pay_list_temp = {}
create_role_list = {}
before_pay_list = {}
game_info = {}

for pmv in pmresult:
    game = pmv['game']
    area = pmv['area']
    plat = pmv['plat']
    print pmv
    if not area in game_info.keys():
        if not game in user_pay_list.keys():
            user_pay_list[game] = {}
            user_pay_list_temp[game] = {}
        user_pay_list[game][area] = {plat : [pmv['user'], ]}
        user_pay_list_temp[game][area] = {
            plat : {
                'user' : {pmv['user'] : 1},
                'pay_amout' : {pmv['user'] : pmv['rmb']}
            }
        }
        game_info[area] = 1

    elif not plat in user_pay_list[game][area].keys():
        user_pay_list[game][area][plat] = [pmv['user'], ]
        user_pay_list_temp[game][area][plat] = {
                'user' : {pmv['user'] : 1},
                'pay_amout' : {pmv['user'] : pmv['rmb']}
        }
    else:
        user_pay_list[game][area][plat].append(pmv['user'])
        if not 'user' in user_pay_list_temp[game][area][plat].keys():
            user_pay_list_temp[game][area][plat]['user'] = {pmv['user'] : 1}
            user_pay_list_temp[game][area][plat]['pay_amout'] = {pmv['user'] : pmv['rmb']}
        else:
            user_pay_list_temp[game][area][plat]['user'][pmv['user']] = 0
            user_pay_list_temp[game][area][plat]['pay_amout'][pmv['user']] += pmv['rmb']
        #????
        user_pay_list_temp[game][area][plat]['user'][pmv['user']] += 1
        user_pay_list_temp[game][area][plat]['pay_amout'][pmv['user']] += pmv['rmb']
            
            
search = {'ts' : {'$gte' : start,'$lte' : end}}

create_role_data = ucrm.get_list(search)
for role in create_role_data:
    game = role['game']
    area = role['area']
    plat = role['plat']
    ts = role['ts']
    
    if game not in create_role_list.keys():
        create_role_list[game] = {area : {plat : role['userlist']}}

    elif area not in create_role_list[game].keys():
        create_role_list[game][area] = {plat : role['userlist']}

    elif plat not in create_role_list[game][area].keys():
        create_role_list[game][area][plat] = role['userlist']

before_pay_data = poulm.get_list()
for bpould in before_pay_data:
    game = bpould['game']
    area = bpould['area']
    plat = bpould['plat']
    userlist = bpould['userlist']
    
    if game not in before_pay_list.keys():
        before_pay_list[game] = {area : {plat : []}}

    elif area not in before_pay_list[game].keys():
        before_pay_list[game][area] = {plat : []}
    elif plat not in before_pay_list[game][area].keys():
        before_pay_list[game][area][plat] = []

    before_pay_list[game][area][plat] += userlist
    before_pay_list[game][area][plat] = list(set(before_pay_list[game][area][plat]))

area = am.get_list()
for item in area:
    for plat in item['plats']:
        game = item['game']
        area = str(item['_id'])
        userlist_pay_today_create_role = {}
        userlist_pay_before_create_role = {}

        try:
            userlist_pay_today_create_role = dict.fromkeys([x for x in \
                user_pay_list[game][area][plat] if x in create_role_list[game][area][plat]])
            userlist_pay_before_create_role = dict.fromkeys([x for x in \
                user_pay_list[game][area][plat] if x not in create_role_list[game][area][plat]])

            old_user_pay_order = dict.fromkeys([x for x in \
                userlist_pay_before_create_role[game][area][plat] if x in before_pay_list[game][area][plat]])
            new_user_pay_order = dict.fromkeys([x for x in \
                userlist_pay_before_create_role[game][area][plat] if x not in before_pay_list[game][area][plat]])
        except KeyError:
            pass

        fix_data = {
            'area' : area,
            'game' : game,
            'plat' : plat,
            'ts' : start
        }

        __id = uptdm.get_one(fix_data, {'_id'})

        fix_data['old_pay_user_count'] = len(old_user_pay_order)
        fix_data['old_pay_user_count_a'] = 0
        fix_data['old_pay_user_amout'] = 0
        fix_data['new_pay_user_count'] = len(new_user_pay_order)
        ##新用户充值次数 
        fix_data['new_pay_user_count_a'] = 0
        ##新用户充值金额
        fix_data['new_pay_user_amout'] = 0
        
        ##当日总充值人数
        fix_data['today_total_pay_user_count'] = len(user_pay_list[game][area][plat])

        ##当日充值人数
        fix_data['today_creatrole_pay_user_count'] = len(userlist_pay_today_create_role)
        
        ##当日的创建角色数
        fix_data['today_creatrole_count'] = len(create_role_list[game][area][plat])


        for acctid in old_user_pay_order:
            fix_data['old_pay_user_count_a'] += user_pay_list_temp[game][area][plat]['user'][acctid]
            fix_data['old_pay_user_amout'] += user_pay_list_temp[game][area][plat]['pay_amout'][acctid]


    
        for acctid in new_user_pay_order:
            fix_data['new_pay_user_count_a'] += user_pay_list_temp[game][area][plat]['user'][acctid]
            fix_data['new_pay_user_amout'] += user_pay_list_temp[game][area][plat]['pay_amout'][acctid]


        if __id:
            id = str(__id['_id'])
            uptdm.update(id, fix_data)
        else:
            uptdm.insert(fix_data)


print time.ctime(), __file__, ' stop...'
