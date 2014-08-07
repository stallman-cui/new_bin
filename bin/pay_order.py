#!/usr/bin/env python
#-*-coding:utf-8-*-
# This program is used to anlytics yuanbao_logchange
# gamelog, and write some infomation to analytics.pay_order
# 2014-07-25
# author: zwcui   cuizhw@millionhero.com

import time, sys
reload(sys)
sys.path.append('..')
sys.setdefaultencoding('utf-8')

from models import gamelogmodel, areamodel, platmodel, payordermodel

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

glm = gamelogmodel.GameLogModel()
am = areamodel.AreaModel()
pm = platmodel.PlatModel()
pom = payordermodel.PayOrderModel()

game_info = {}
search = {
    'op.code' : 'yuanbao_logchange',
    'ts' : {'$gte' : start , '$lte' : end}
}
data = glm.get_list(search)

for d in data:
    try:
        d['data']['extra']['reqstr']
    except KeyError:
        continue

    area = d['area']
    plat = d['data']['CorpId']
    if not area in game_info.keys():
        area_info = am.get_by_idstr(area)
        game_info[area] = area_info['game']
        game = game_info[area]

    game = game_info[area]
    search = {
        'game' : game,
        'area' : area,
        'plat' : plat,
        'orderid' : d['data']['extra']['reqstr']
    }
    __id = pom.get_one(search, {'_id'})
    ## 充值前元宝
    search['paybeforeyuanbao'] = d['data']['extra']['new_yuanbao'] - d['data']['amount']
    search['payafteryuanbao'] = d['data']['extra']['new_yuanbao']
    search['Uid'] = d['data']['Uid']
    search['Name'] = d['data']['Name']
    
    if __id:
        mid = str(__id['_id'])
        pom.update(mid, search)
    else:
        pom.insert(search)

print time.ctime(), __file__, ' stop...'
