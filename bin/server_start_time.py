#!/usr/bin/env python
#-*-coding:utf-8-*-
# This program is used to anlytics server start time, read data 
# from gamelog, and write some infomation to analytics.server_start_time
# 2014-07-25
# author: zwcui   cuizhw@millionhero.com

import time
import sys
reload(sys)
sys.path.append('..')
sys.setdefaultencoding('utf-8')
from models import gamelogmodel, areamodel, serverstartmodel

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
sstm = serverstartmodel.ServerStartTimeModel()

search = {
    'op.code' : 'login_logcount',
    'ts' : {'$gte' : start , '$lte' : end}
}
data = glm.get_list(search)
game_info = {}
server_start = {}

for d in data:
    area = d['area']
    plat = d['data']['corpid']

    # Check if the area is not set one area is only owned by one game
    if not area in game_info.keys():
        area_info = am.get_by_idstr(area)
        game_info[area] = area_info['game']
        game = game_info[area]
        if not game in server_start.keys():
            server_start[game] = {}
        server_start[game][area] = {plat : d['ts']}

    else:
        game = game_info[area]
        if not plat in server_start[game][area].keys():
            server_start[game][area][plat] = d['ts']
        elif server_start[game][area][plat] > d['ts']:
            server_start[game][area][plat] = d['ts']

for kgame, vgame in server_start.items():
    for karea, varea in vgame.items():
        for kplat, vplat in varea.items():
            fix_data = {
                'game' : kgame,
                'area' : karea,
                'plat' : str(kplat)
            }
            __id = sstm.get_one(fix_data, {'_id', 'area'})
            fix_data['server_start_time'] = vplat
            if not __id:
                sstm.insert(fix_data)

print time.ctime(), __file__, ' stop...'
