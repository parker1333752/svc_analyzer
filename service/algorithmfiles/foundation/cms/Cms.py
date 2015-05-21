from MongoNodeService import TxMongoNodeService
from RawStorageService import TxRawStorageService

class TxCms(object):
    '''
    storageConfig format:
        storageConfig = {
            'RawStorageService':{
                'ssid':'rootdir',
            },
        }
    '''
    def __init__(self,mongodb,storagesConfig):
        self.__storages = {}

        if storagesConfig.has_key('RawStorageService'):
            for i,v in storagesConfig['RawStorageService'].iteritems():
                self.__storages[i] = TxRawStorageService(v)

        self.__nodes = TxMongoNodeService(mongodb.nodes,self.__storages)

    def getNodes(self):
        return self.__nodes

    def getSsids(self):
        return self.__storages.keys()
