from common.mongo import MongoModel

class PropUserModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'prop_user_list'
