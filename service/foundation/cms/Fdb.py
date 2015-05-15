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
    def __init__(self, nodes_rootdir, storagesConfig):
        self.__storages = {}

        if storagesConfig.has_key('RawStorageService'):
            for i,v in storagesConfig['RawStorageService'].iteritems():
                self.__storages[i] = TxRawStorageService(v)

        self.__nodes = TxFdbNodeService(nodes_rootdir, self.__storages)

    def getNodes(self):
        return self.__nodes

    def getSsids(self):
        return self.__storages.keys()

if __name__ == '__main__':
    '''for test'''
    #config = {'RawStorageService':{'Rawdata':'/'}}
    config = {}
    a = TxFdb('/',config)
    print dir(a)
    print 
    print a.getSsids()
    print a.getNodes()
