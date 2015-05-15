from RawStorageFile import TxRawStorageFile
import os

class TxRawStorageService(object):
    config = {
        'hash_length':8,
        }
    def __init__(self, rootdir):
        self.rootdir = rootdir

    def __getPath(self, id_):
        path = self.rootdir
        path += '/' + id_[:self.__class__.config['hash_length']]

        if not os.path.exists(path):
            os.makedirs(path)

        path += '/' + id_
        return path

    def newItem(self, id_):
        if id_ == None:
            return

        path = self.__getPath(id_)
        return TxRawStorageFile(path)

    def getFile(self,id_):
        print 'hellolololasdfdso'
        return self.newItem(id_)

    def remove(self, id_):
        path = self.__getPath(id_)

        try:
            os.remove(path)
        except:
            return

        try:
            folder = os.path.split(path)[0]
            os.rmdir(folder) # if folder is empty, remove the folder
        except:
            pass

    def save(self, id_, data):
        storageFile = self.newItem(id_)
        return storageFile.save(data)

    def load(self, id_):
        storageFile = self.newItem(id_)
        return storageFile.load()
