#!/usr/bin/env python
#import time
import sys, re, json, time
reload(sys)
sys.path.append('..')
sys.setdefaultencoding('utf-8')
from models import gamelogmodel
glm = gamelogmodel.GameLogModel()
FORMAT = '%Y-%m-%d %H:%M:%S'

for line in sys.stdin.readlines():
    line = line.strip()
    m = re.match(r'(\w+)\t\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]\t(.*)', line)
    if not m:
        continue
    data = json.loads(m.group(3))
    #print json.dumps(data, indent=3)
    if data.get('opname', 0) and data.get('opno', 0):
        area = m.group(1)
        ts = time.strptime(m.group(2), FORMAT)
        ts = int(time.mktime(ts))

        fix_data = {
            'op' : {
                'code' : data['opname'],
                'id'   : data['opno']
            },
            'area' : area,
            'ts' : ts,
            'data' : data
        }
        glm.insert(fix_data)
