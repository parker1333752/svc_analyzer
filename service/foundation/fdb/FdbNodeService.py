from Node import TxNode
import uuid

class TxFdbNodeService(object):
    def __init__(self,storages):
        self.storages = storages

    def newId(self):
        id_ = str(uuid.uuid1()).replace('-','')
        return id_

    def newItem(self, ssid,  id_):

        storage = self.storages.get(ssid)
        if storage == None:
            raise AssertionError, 'storage <%s> not exists'%ssid

        node = TxNode(id_,storage)

        return node

    def copy(self, dstNode, srcNode):
        '''TODO finish this'''
        pass

    def getStorageService(self, ssid):
        return self.storages.get(ssid)

