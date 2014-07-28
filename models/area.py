from mongo import MongoModel

class AreaModel(MongoModel):
    def get_db(self):
        return 'game'

    def get_collection(self):
        return 'area'
