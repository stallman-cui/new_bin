from common.mongo import MongoModel

class ServerStartTimeModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'server_start_time'

