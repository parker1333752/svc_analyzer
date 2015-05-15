from pymongo import MongoClient
from fdb.Fdb import TxFdb
import Config

class TxAppService:
    def __init__(self):
        self.__config = Config.get_config()

    def getMongoClient(self):
        try:
            value = self.__mongoClient
        except:
            self.__mongoClient = MongoClient(self.__config['mongohost'],self.__config['mongoport'])

        return self.__mongoClient

    def getFdb(self):
        try:
            value = self.__fdb
        except:
            self.__fdb = TxFdb(self.__config['fdbStorages'])

        return self.__fdb
