from common.mongo import MongoModel

class CoinTypeModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'coin_type'
