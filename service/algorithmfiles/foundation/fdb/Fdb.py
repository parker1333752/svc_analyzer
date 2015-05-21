from FdbNodeService import TxFdbNodeService
from RawStorageService import TxRawStorageService

class TxFdb(object):
    '''
    - storagesConfig format:
        storagesConfig = {
            'RawStorageService':{
                'ssid':'rootdir',
            },
        }
    '''
    def __init__(self, storagesConfig):
        self.__storages = {}

        if storagesConfig.has_key('RawStorageService'):
            for i,v in storagesConfig['RawStorageService'].iteritems():
                self.__storages[i] = TxRawStorageService(v)

        self.__nodes = TxFdbNodeService(self.__storages)

    def getNodes(self):
        return self.__nodes

    def getSsids(self):
        return self.__storages.keys()

