#!/usr/bin/env python
#-*-coding:utf-8-*-
# This program is used to anlytics mainline task from
# gamelog, and write some data to analytics.mainline
# 2014-07-25
# author: zwcui   cuizhw@millionhero.com

import time, sys
reload(sys)
sys.path.append('..')
sys.setdefaultencoding('utf-8')

from models import gamelogmodel, areamodel
from models import mainlineusermodel, mainlinemodel

print time.ctime(), __file__, ' start...'
FORMAT = '%Y-%m-%d'
if len(sys.argv) == 1:
    now = time.strftime(FORMAT, time.localtime())
else:
    now = sys.argv[1] 
today = time.strptime(now, FORMAT)
end = int(time.mktime(today)) - 1
start = end - 3600 * 24 + 1

glm = gamelogmodel.GameLogModel()
am = areamodel.AreaModel()
mum = mainlineusermodel.MainlineUserModel()
mm = mainlinemodel.MainlineModel()
game_info ={}
mainline = {}
yes_accept_user = {}
yes_finish_user = {}

search = {
    'op.code' : {'$in' : ['trunk_task_accept', 'trunk_task_finish']},
    'ts' : {'$gte' : start, '$lte' : end}
}

data = glm.get_list(search)
for d in data:
    area = d['area']
    plat = d['data']['CorpId']
    acctid = d['data']['URS'].split('_')[0]
    taskid = d['data']['task_id']
    op_code = d['op']['code']

    if not area in game_info.keys():
        area_info = am.get_by_idstr(area)
        game_info[area] = area_info['game']
        game = game_info[area]

        if not game in mainline.keys():
            mainline[game] = {}
            yes_accept_user[game] = {}
            yes_finish_user[game] = {}

        mainline[game][area] = {
            plat : {
                taskid : d['data']['task_name']
            }
        }

        yes_accept_user[game][area] = {
            plat : {
                taskid : []
            }
        }
        yes_finish_user[game][area] = {
            plat : {
                taskid : []
            }
        }
        
    else:
        game = game_info[area]
        if not plat in mainline[game][area].keys():
            mainline[game][area][plat] = {
                taskid : d['data']['task_name']
            }
            yes_accept_user[game][area][plat] = {taskid : []}
            yes_finish_user[game][area][plat] = {taskid : []}

        elif not taskid in mainline[game][area][plat].keys():
            mainline[game][area][plat][taskid] = d['data']['task_name']
            yes_accept_user[game][area][plat][taskid] = []
            yes_finish_user[game][area][plat][taskid] = []

    search = {
        'area' : area,
        'plat' : str(plat), 
        'ts' : start - 3600 * 24,
        'taskid' : taskid
    }
    
    re = mum.get_one(search, {'acceptuserlist' : 1, 'finishuserlist' : 1})
    if 'trunk_task_accept' == op_code:
        if re and 'acceptuserlist' in re.keys():
            yes_accept_user[game][area][plat][taskid] = re['acceptuserlist']
        if not acctid in yes_accept_user[game][area][plat][taskid]:
            yes_accept_user[game][area][plat][taskid].append(acctid)
    else:
        if re and 'finishuserlist' in re.keys():
            yes_finish_user[game][area][plat][taskid] = re['finishuserlist']
        if not acctid in yes_finish_user[game][area][plat][taskid]:
            yes_finish_user[game][area][plat][taskid].append(acctid)

for kgame, vgame in mainline.items():
    for karea, varea in vgame.items():
        for kplat, vplat in varea.items():
            for ktask, vtask in vplat.items():
                search = {
                    'area' : karea,
                    'plat' : str(kplat), 
                    'ts' : start,
                    'taskid' : ktask
                }

                __id = mum.get_one(search, {'_id' : 1})
                acc = {}
                fin = {}
                try:
                    acc = yes_accept_user[kgame][karea][kplat][ktask]
                    fin = yes_finish_user[kgame][karea][kplat][ktask]
                except KeyError:
                    pass
                
                search['acceptuserlist'] = acc
                search['finishuserlist'] = fin
                
                if __id:
                    mid = str(__id['_id'])
                    mum.update(mid, search)
                else:
                    mum.insert(search)
                
                fix_data = {
                    'game' : kgame,
                    'plat' : str(kplat),
                    'area' : karea,
                    'ts' : start,
                    'taskid' : ktask
                }
                __id = mm.get_one(fix_data, {'_id' : 1})
                fix_data['name'] = vtask
                fix_data['accept_user'] = len(acc)
                fix_data['finish_user'] = len(fin)

                if __id:
                    mid = str(__id['_id'])
                    mm.update(mid, fix_data)
                else:
                    mm.insert(fix_data)

print time.ctime(), __file__, ' stop...'
