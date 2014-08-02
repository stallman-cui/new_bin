from common.mongo import MongoModel

class ServerModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'server'
