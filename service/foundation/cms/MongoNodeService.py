import pymongo
class TxMongoNodeService(object):
    def __init__(self,collection,storages):
        self.collection = collection
        self.storages = storages

    def newItem(self, id_):
        return TxNode()

    def add(self, inputNode):
        id_ = None
        return id_

    def get(self, id_):
        return TxNode()

    def set(self, id_, inputNode):
        pass

    def remove(self, id_):
        pass

    def getStorageService(self, ssid):
        return self.storages.get(ssid)

    def save(self, id_, data):
        pass

    def load(self, id_):
        data = ''
        return data
