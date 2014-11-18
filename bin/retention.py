#!/usr/bin/env python
#-*-coding:utf-8-*-
# 2014-07-25
# author: zwcui   cuizhw@millionhero.com

import time, sys
reload(sys)
sys.path.append('..')
sys.setdefaultencoding('utf-8')
from models import usercreaterolemodel, userloginmodel, usernumretentionmodel

print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), __file__, ' start...'

FORMAT = '%Y-%m-%d'
if len(sys.argv) == 1:
    now = time.strftime(FORMAT, time.localtime())
else:
    now = sys.argv[1] 
today = time.strptime(now, FORMAT)
end = int(time.mktime(today)) - 1
start = end - 3600 * 24 + 1

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
search = {'ts' : {'$gte' : re_time[0]['start'],'$lte' : re_time[0]['end']}}

login_data = ulm.get_list(search)
for d in login_data:
    login_list = {}
    if d.get('userlist', 0):
         login_list = d['userlist']
    else:
        continue

    search = {
            'area' : str(d['area']),
            'plat' : str(d['plat']),
            'ts' : {'$gte' : re_time[0]['start'],'$lte' : re_time[0]['end']}
    }
    create_role = ucrm.get_one(search, {'_id' : 1, 'count' : 1})
    if create_role:
        user_total = create_role['count']
    else:
        user_total = 0

    fix_data = {
        'area' : str(d['area']),
        'game' : d['game'],
        'plat' : str(d['plat']),
        'ts' : start
    }

    __id = unrm.get_one(fix_data, {'_id' : 1})
    fix_data['user'] = user_total
    if __id:
        mid = str(__id['_id'])        
        unrm.update(mid, fix_data)
    else:
        unrm.insert(fix_data)

    for i in range(1, 31):
        if i <= 7 or i == 14 or i == 30:
            search = {
                'area' : str(d['area']),
                'plat' : str(d['plat']),
                'ts' : {'$gte' : re_time[i]['start'],'$lte' : re_time[i]['end']}
            }
            create_role = ucrm.get_one(search, {'_id' : 1, 'userlist' : 1})
            if create_role:
                create_role_list = create_role['userlist']
                if len(create_role_list) < len(login_list):
                    user_fix = dict.fromkeys([x for x in create_role_list if x in login_list])
                else: 
                    user_fix = dict.fromkeys([x for x in login_list if x in create_role_list ])
            else:
                continue

            if not len(user_fix):
                continue
                        
            fix_data = {
                'game' : d['game'],
                'area' : str(d['area']),
                'plat' : str(d['plat']),
                'ts' : re_time[i]['start']
            }
            __id = unrm.get_one(fix_data, {'_id' : 1})
            fix_data[str(i) + '_retention'] = len(user_fix)
                
            if __id:
                mid = str(__id['_id'])
                unrm.update(mid, fix_data)
            else:
                unrm.insert(fix_data)
                    
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), __file__, ' stop...'
