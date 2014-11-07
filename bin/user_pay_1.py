#!/usr/bin/env python
#-*-coding:utf-8-*-
# This program is used to anlytics user pay, read data from gamelog,
# and write some infomation to user_pay
# 2014-07-25
# author: zwcui   cuizhw@millionhero.com

import time, sys, json
reload(sys)
sys.path.append('..')
sys.setdefaultencoding('utf-8')

from models import gamelogmodel, platmodel, areamodel

FORMAT = '%Y-%m-%d'
print time.ctime(), __file__, ' start...'

if len(sys.argv) == 1:
    now = time.strftime(FORMAT, time.localtime())
else:
    now = sys.argv[1] 

today = time.strptime(now, FORMAT)
end = int(time.mktime(today)) - 1
start = end - 3600 * 24 + 1

glm = gamelogmodel.GameLogModel()
am = areamodel.AreaModel()
pm = platmodel.PlatModel()

search = {
    'op.code' : 'yuanbao_logchange',
    'ts' : {'$gte' : start , '$lte' : end}
}
data = glm.get_list(search)
user = {}
for d in data:
    if not 'reqstr' in d['data']['extra'].keys():
        continue

    area = d['area']
    plat = d['data']['CorpId']
    uid = d['data']['Uid']
    area_info = am.get_by_idstr(area)
    if not area_info:
        continue
    plat_info = pm.get_by_id(str(plat))
    game = area_info['game']
    
    # If it is found in the first time
    if not user.get(uid, 0):
        search = {
            'game' : game,
            'plat' : plat,
            'area' : area,
            'uid' : uid
        }
        
        # search all the record of use yuanbao
        search = {
            "op.code" : "yuanbao_logchange",
            'ts' : {'$gte' : start, '$lte' : end}
        }
        
        documents = glm.get_list(search)
        used_yuanbao = 0
        for each_data in documents:
            if each_data['data']['CorpId'] != int(plat) and \
                   each_data['data']['Uid'] != str(uid) and \
                   each_data['area'] != area:
                continue
            else:
                if each_data['data']['amount'] < 0:
                    used_yuanbao += -each_data['data']['amount']
                # search all the record of use yuanbao
        search = {
            "op.code" : "yuanbao_logchange",
            'ts' : {'$gte' : start, '$lte' : end}
        }
        
        documents = glm.get_list(search)
        used_yuanbao = 0
        for each_data in documents:
            if each_data['data']['CorpId'] != int(plat) and \
                   each_data['data']['Uid'] != str(uid) and \
                   each_data['area'] != area:
                continue
            else:
                if each_data['data']['amount'] < 0:
                    used_yuanbao += -each_data['data']['amount']

        search = {
            'game' : game,
            'plat' : plat,
            "area" : area,		
            'uid' : str(uid)
        }

        pay_doc  = apm.get_one(search, {"_id" : 1, "firstPayGrade" : 1})
        if  pay_doc:
            first_pay_grade = pay_doc['firstPayGrade']
        else:
            first_pay_grade = d['data']['Grade']
        user[uid] = {
            'game' : game,
            'area' : area,
            'plat' : plat,
            'grade' : d["data"]["Grade"],
            'name' : d["data"]["Name"],
            'rest_yuanbao' : rest_yuanbao,
            'count' : 0,
            'amout' : 0,
            'yuanbao' : 0,
            'reg_time' : reg_time,
            'recent_login' : recent_login,
            'used_yuanbao' : used_yuanbao,
            'first_pay_grade' : first_pay_grade
        }
        

    # if it was founded once
    else:
        user[uid]['count'] += 1
        user[uid]['amout'] += d['data']['amount'] / 10
        user[uid]['yuanbao'] += d['data']['amount']

print json.dumps(user)
