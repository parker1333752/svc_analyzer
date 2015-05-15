from pymongo import MongoClient
from fdb.Fdb import TxFdb
import Config

class TxAppService:
    def __init__(self):
        config = Config.get_config()
        self.mongoClient = MongoClient(config['mongohost'],config['mongoport'])
        #self.cms = TxCms(self.mongoClient['test'], config['cmsStorages'])
        self.fdb = TxFdb(config['fdbStorages'])
