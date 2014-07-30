from ninny import NinnyGhokoModel
from config import db_config

class GhokoModel(NinnyGhokoModel):
    __ghoko = ''

    def pass_method(self, method, query, param, url = ''):
        if not self.__ghoko:
            self.__ghoko = NinnyGhokoModel()
