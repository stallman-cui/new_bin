from common.mongo import MongoModel

class PayOrderModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'pay_order'
