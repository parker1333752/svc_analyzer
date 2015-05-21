from pymongo import MongoClient
from fdb.Fdb import TxFdb
from cms.Cms import TxCms
import config

class TxAppService:
    def __init__(self):
        #self.__config = Config.get_config()
        self.__config = config.globalConfig

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

    def getCms(self):
        try:
            value = self.__cms
        except:
            self.__cms = TxCms(self.getMongoClient()['test'], self.__config['cmsStorages'])

        return self.__cms
