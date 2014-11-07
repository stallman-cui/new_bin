#!/usr/bin/env python
#-*-coding:utf-8-*-

import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')

from models import hostmodel

hm = hostmodel.HostModel()

hosts = hm.get_list({'flag.available' : True})
for host in hosts:
    print("%s" % host['id']),

