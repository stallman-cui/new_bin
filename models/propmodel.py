from common.mongo import MongoModel

class PropModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'prop'
