from common.mongo import MongoModel

class UserPayTraceDayModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'user_pay_trace_day'
