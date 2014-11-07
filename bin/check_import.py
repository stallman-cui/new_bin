#!/usr/bin/env python

import time, sys
reload(sys)
sys.path.append('..')
sys.setdefaultencoding('utf-8')

if len(sys.argv) >= 2:
    server = "002_h_user"
else:
    server = ""

from models import gamelogmodel
glm = gamelogmodel.GameLogModel(server)

FORMAT = '%Y-%m-%d %H:%M'
now = sys.argv[1] 

begin = time.strptime(now, FORMAT)
begin = int(time.mktime(begin))
stop = int(time.time()) - 600

print begin, stop

check_time = {}

i = 0
start = begin
while 1:
    if start >= stop:
        break

    check_time[i] = {
        'start' : start,
        'end' : start + 3600,
    }
    start += 3600
    i = i + 1

for i in range(len(check_time)):
    search = {
        'ts' : {
            '$gte': check_time[i]['start'],
            '$lte': check_time[i]['end']
        }
    }
    print search
    count = glm.get_list(search).count()
    print i, count
