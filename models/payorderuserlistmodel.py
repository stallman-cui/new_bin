from common.mongo import MongoModel

class PayOrderUserListModel(MongoModel):
    def get_db(self):
        return 'analytics'

    def get_collection(self):
        return 'pay_order_user_list'
