from common.mongo import MongoModel

class MainlineUserModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'mainline_user_list'
