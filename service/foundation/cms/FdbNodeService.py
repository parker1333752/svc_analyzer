from Node import TxNode
import json
import uuid
import os

class TxFdbNodeService(object):
    config = {
        'hash_length':8,
        }
    def __init__(self,rootdir,storages):
        self.rootdir = rootdir
        self.storages = storages

    def __autoId(self, ):
        id_ = str(uuid.uuid1()).replace('-','')
        return id_

    def __getPath(self, id_):
        path = self.rootdir
        path += '/' + id_[:self.__class__.config['hash_length']]

        if not os.path.exists(path):
            os.makedirs(path)

        path += '/' + id_ + '.json'
        return path

    def newItem(self, id_ = None):
        node = TxNode()

        if id_:
            node.id_ = id_
        else:
            node.id_ = self.__autoId()

        return node

    def add(self, inputNode):
        if inputNode.id_ == None:
            inputNode.id_ = self.__autoId()

        path = self.__getPath(inputNode.id_)
        fd = open(path,'w')
        json.dump(inputNode.__dict__ , fd,indent=4,sort_keys=True)
        fd.close()

        return inputNode.id_

    def get(self, id_):
        path = self.__getPath(id_)

        nodeInfo = None
        try:
            fd = open(path,'r')
            nodeInfo = json.load(fd)
            fd.close()
        except:
            print 'node not exist'
            return

        node = TxNode()
        for i in nodeInfo.iterkeys():
            if node.__dict__.has_key(i):
                node.__dict__[i] = nodeInfo[i]

        return node

    def set(self, id_, inputNode):
        node = self.get(id_)
        inputNode.id_ = None # prevent id_ to be modified

        for i,v in inputNode.__dict__.iteritems():
            if v != None and i in node.__dict__.iterkeys():
                node.__dict__[i] = v

        self.add(node)

    def remove(self, id_):
        path = self.__getPath(id_)

        node = self.get(id_)
        if node == None:
            print 'node not exist'
            return

        try:
            os.remove(path)
        except:
            return

        try:
            folder = os.path.split(path)[0]
            os.rmdir(folder) # if folder is empty, remove the folder
        except:
            pass

        storageService = self.getStorageService(node.ssid)
        if storageService == None:
            print 'storage service[%s] not exist'%(node.ssid)
            return

        storageService.remove(id_)

    def getStorageService(self, ssid):
        return self.storages.get(ssid)

    def getFile(self,id_):
        node = self.get(id_)
        if node == None:
            #raise AssertionError, 'node not exist'
            print 'node not exist'
            return

        storageService = self.getStorageService(node.ssid)
        if storageService == None:
            #raise AssertionError, 'storage service[%s] not exist'%(node.ssid)
            print 'storage service[%s] not exist'%(node.ssid)
            return

        return storageService.getFile(id_)

    def save(self, id_, data):
        '''save storage file content.
        '''
        if type(id_) == self.__class__:
            id_ = id_.id_

        storageFile = self.getFile(id_)

        return storageFile.save(data)

    def load(self, id_):
        '''load storage file content.
        '''
        storageFile = self.getFile(id_)

        return storageFile.load()

if __name__ == '__main__':
    '''for test'''
    a = TxNode()
    print type(a) == a.__class__
