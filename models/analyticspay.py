from mongo import MongoModel

class AnalyticsPayModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'user_pay'
