from common.mongo import MongoModel

class GameCopyUserModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'game_copy_user_list'
