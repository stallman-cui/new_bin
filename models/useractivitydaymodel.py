from common.mongo import MongoModel

class UserActivityDayModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'user_activity_day'
