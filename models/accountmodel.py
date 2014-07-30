from common.mongo import MongoModel
from bson import ObjectId
from models import areamodel, hostmodel

class AccountModel(MongoModel):
    def get_db(self):
        return 'game'

    def get_collection(self):
        return 'account'

    def get_one(self, search = {}):
        data = super.get_one(search)
        if not data:
            s = {
                'game' : search['game_tag'],
                'plats' : search['plat_id'],
                '_id' :  ObjectId(search['area_id'])
            }
            am = areamodel.AreaModel()
            area = am.get_one(search = s)
            if not area:
                return {}
            hm = hostmodel.HostModel()
            host = hm.get_one(search = {'id' : area['host']})
            if not host:
                return {}

            if search.get('info', 1):
                search['info'] = ""
            
            params = {
                'port'	: area['port']['mcs'],
                'game'	: search['game_tag'],
                'plat'	: search['plat_id'],
                'area'	: search['area_id'],
                'account' : search['account'],
                'char' : search['char'],
                'info' : search['info']
            }

            acct = 
