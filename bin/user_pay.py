#!/usr/bin/env python
# coding=UTF-8
# This program is used to anlytics user pay, read data from gamelog,
# and write some infomation to user_pay
# 2014-07-25
# author: zwcui   cuizhw@millionhero.com

import time
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

sys.path.append('..')
from models import gamelogmodel, platmodel, areamodel
from models import analyticspaymodel, accountmodel
FORMAT = '%Y-%m-%d'

if len(sys.argv) == 1:
#    now = time.strftime(FORMAT, time.localtime())
    now = '2014-7-30'
else:
    now = sys.argv[1] 

today = time.strptime(now, FORMAT)
end = int(time.mktime(today)) - 1
start = end - 3600 * 24 + 1

glm = gamelogmodel.GameLogModel()
am = areamodel.AreaModel()
pm = platmodel.PlatModel()
apm = analyticspaymodel.AnalyticsPayModel()

search = {
    'op.code' : 'yuanbao_logchange',
    'ts' : {'$gte' : start , '$lte' : end}
}

data = glm.get_list(search)
user = {}

for d in data:

    try: 
        d['data']['extra']['reqstr']
    except KeyError, e:
        continue
    print 'begin: ', user

    area = d['area']
    plat = d['data']['CorpId']

    '''
    area_info = am.get_by_idstr(area)
    plat_info = pm.get_by_id(str(plat))

    game = area_info['game']
    '''
    uid = d['data']['Uid']
    if not user.get(uid, 0):
        area_info = am.get_by_idstr(area)
        plat_info = pm.get_by_id(str(plat))
        game = area_info['game']
        
        rest_yuanbao = 0

        account = {'id' : '', 'name' : ''}
        char = {'id' : uid, 'name' : ''}

        search = {
            'game_tag' : game,
            'plat_id' : plat,
            'area_id' : area,
            'account' : account,
            'char' : char,
            'info' : {'acct' : 1}
        }

        acm = accountmodel.AccountModel()
        try:
            userdata = acm.get(search)
        except Exception, e:
            print(search)
            print(e.message)
            try:
                userdata = acm.get(search)
            except Exception,e:
                print(search)
                print e.message
                continue


        user[uid] = {
            'game' : game,
            'area' : area,
            'plat' : plat,
            'grade' : d["data"]["Grade"],
            'name' : d["data"]["Name"],
            'count' : 0,
            'amout' : 0,
            'yuanbao' : 0
        }

        

    break
    u = {}
    user_plat = {}
    user_area = {}

    u['grade'] = d['data']['Grade']
    u['name'] = d['data']['Name']


    user_plat[uid] = u
    user_area[plat] = user_plat
    user[area] = user_area

    '''
    user[d['area']] = {
        plat : {
            uid : {
                'grade' : d['data']['Grade'],
                'name' : d['data']['Name']
            }
        }
    }
    '''
    if not 'count' in user[area][plat][uid].keys():
        user[area][plat][uid]['count'] = 0
    user[area][plat][uid]['count'] += 1
    
    if not 'amout' in user[area][plat][uid].keys():
        user[area][plat][uid]['amout'] = 0
    user[area][plat][uid]['amout'] += d['data']['amount'] / 10

    if not 'yuanbao' in user[area][plat][uid].keys():
	user[area][plat][uid]['yuanbao'] = 0
    user[area][plat][uid]['yuanbao'] += d['data']['amount']

    print 'end: ', user, '\n\n'

print user
