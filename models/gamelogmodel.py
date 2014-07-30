from common.mongo import MongoModel

class GameLogModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'gamelog'
