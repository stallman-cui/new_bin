from common.mongo import MongoModel

class GameUserModel(MongoModel):
    def get_db(self):
        return 'mhgame'

    def get_collection(self):
        return 'user'
