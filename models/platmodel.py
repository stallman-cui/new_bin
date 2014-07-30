from common.mongo import MongoModel

class PlatModel(MongoModel):
    def get_db(self):
        return 'game'

    def get_collection(self):
        return 'plat'

    def get_by_id(self, id):
        return self.get_one({'id' : id})

if __name__ == "__main__":
    print PlatModel().get_db()
