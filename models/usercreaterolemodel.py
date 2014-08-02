from common.mongo import MongoModel

class UserCreateRoleModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'user_create_role'
