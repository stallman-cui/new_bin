from common.mongo import MongoModel

class UserPayTraceModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'user_pay_trace'
