from common.mongo import MongoModel

class CoinDayModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'coin_day'
