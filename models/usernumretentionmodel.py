from common.mongo import MongoModel

class UserNumRetentionModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'user_num_retention'
