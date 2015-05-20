from MongoNode import TxMongoNode
from pymongo import MongoClient
import uuid

class TxMongoNodeService(object):
    def __init__(self,collection,storages):
        self.collection = collection
        self.storages = storages

    def newId(self):
        id_ = str(uuid.uuid1()).replace('-','')
        return id_

    def newItem(self, id_=None):
        if id_ == None:
            id_ = self.newId()

        node = TxMongoNode()
        node.id = id_
        return node

    def add(self, inputNode):
        if inputNode.id == None:
            inputNode.id = self.newId()

        self.collection.update({'id':inputNode.id},inputNode.__dict__,upsert = True)

    def get(self, id_):
        iterdata = self.collection.find({'id':id_})

        if iterdata.count() > 0:
            data = iterdata.next()
            node = TxMongoNode()

            for i,v in data.iteritems():
                node.__dict__[i] = v

            return node

        else:
            return None

    def set(self, id_, inputNode):
        if id_ == None:
            raise AssertionError, 'id is non-null'

        inputNode.id = id_
        self.collection.update({'id':inputNode.id},inputNode.__dict__)

    def remove(self, id_):
        iterdata = self.collection.find({'id':id_})
        data = None
        if iterdata.count() > 0:
            data = iterdata.next()

        self.collection.remove({'id':id_})

        if not data:
            return

        storage = self.getStorageService(data.ssid)
        if not storage:
            return

        storage.remove(id_)

    def getStorageService(self, ssid):
        return self.storages.get(ssid)

    def getFile(self,id_):
        node = self.get(id_)
        if not node:
            raise AssertionError, 'node not exists'

        storage = self.getStorageService(node.ssid)
        if not storage:
            raise AssertionError, 'storage<%s> not exists'%node.ssid

        return storage.getFile(id_)

if __name__ == '__main__':
    print 'start'
    mongoClient = MongoClient('192.168.1.153',27017)

    dbcollection = mongoClient.test.nodes
    a = TxMongoNodeService(dbcollection,None)

    cur = dbcollection.find({'id':'123123'})

    for ii in cur:
        print (ii)
    print cur.count()

    #print dir(dbcollection)
    dbcollection.remove({'hello':'lisijun'})
    
    dbcollection.update({'id':'123123'},{'id':'123123','hello':'lisijun'})#,upsert = True)
    #print help(dbcollection.update)

    #dbcollection.save({'id':'123123'})

