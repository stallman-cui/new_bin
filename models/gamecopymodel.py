from common.mongo import MongoModel

class GameCopyModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'game_copy'
