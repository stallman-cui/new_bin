from common.mongo import MongoModel

class MainlineModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'mainline'
