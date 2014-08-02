#!/usr/bin/env python
#-*-coding:utf-8-*-
# This program is used to anlytics new created role, read data 
# from gamelog, and write some infomation to analytics.pay_order_user_list
# 2014-07-25
# author: zwcui   cuizhw@millionhero.com

import time, json, sys
reload(sys)
sys.path.append('..')
sys.setdefaultencoding('utf-8')
from models import areamodel, paymentmodel, payorderuserlistmodel

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

pm = paymentmodel.PaymentModel()
am = areamodel.AreaModel()
poulm = payorderuserlistmodel.PayOrderUserListModel()

user_pay_list = {}
game_info = {}
search = {
    'start' : start,
    'end' : end,
    'page.index' : -1
}
result  = pm.get_user_payment_list(search)
if result['status'] != 500:
    pmresult = json.loads(result['body'])
    for d in pmresult:
        game = d['game']
        area = d['area']
        plat = d['plat']
        if not area in game_info.keys():
            if not game in user_pay_list.keys():
                user_pay_list[game] = {}

            user_pay_list[game][area] = {plat : [d['user'],]}
            game_info[area] = 1
        else:
            if not plat in user_pay_list[game][area].keys():
                user_pay_list[game][area][plat] = [d['user'],]
            else:
                if not d['user'] in user_pay_list[game][area][plat]:
                    user_pay_list[game][area][plat].append(d['user'])

for kgame, vgame in user_pay_list.items():
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

            __id = poulm.get_one(search, {'_id', 'game'})
            search['count'] = len(user_list)
            search['userlist'] = user_list
        
            if __id:
                mid = str(__id['_id'])
                poulm.update(mid, search)
            else:
                poulm.insert(search)

print time.ctime(), __file__, ' stop...'
