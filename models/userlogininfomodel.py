from common.mongo import MongoModel

class UserLoginInfoModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'user_login_info'
