#!/usr/bin/env python
# This program is used to anlytics user pay, read data from gamelog,
# and write some infomation to user_pay
# 2014-07-25
# author: zwcui   cuizhw@millionhero.com

import time
import sys
from bson import ObjectId

sys.path.append('..')
from models import mongo, gamelog, area, plat, analyticspay

FORMAT = '%Y-%m-%d'

if len(sys.argv) == 1:
    now = time.strftime(FORMAT, time.localtime())
else:
    now = sys.argv[1]

today = time.strptime(now, FORMAT)
end = int(time.mktime(today)) - 1
start = end - 3600 * 24 + 1
#print end, '--', start

glm = gamelog.GameLogModel()
am = area.AreaModel()
pm = plat.PlatModel()
apm = analyticspay.AnalyticsPayModel()

search = {
    'op.code' : 'yuanbao_logchange',
    'ts' : {'$gte' : start , '$lte' : end}
}

data = glm.get_list(search = search)
for doc in data:
    if not 'reqstr' in doc['data']['extra'].keys():    
        continue
    
    area = doc['area']
    plat = doc['data']['CorpId']
    by_id = {'_id' : area}
    area_info = am.get_one(_id = area)

    plat_info = pm.get_by_id(plat)
    
    print area, plat, area_info, plat_info
