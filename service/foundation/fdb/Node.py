import json
class TxNode(object):
    def __init__(self,id_,storage):
        self.id = id_
        self.storage = storage

    def loadProperties(self):
        fid = self.id + '.json'

        data = None

        try:
            fileContent = self.storage.load(fid)
            data = json.loads(fileContent)
        except:
            pass

        return data

    def saveProperties(self, properties):
        fid = self.id + '.json'

        data = json.dumps(properties)
        self.storage.save(fid,data)

    def getFile(self):
        return self.storage.getFile(self.id)

    def remove(self):
        self.storage.remove(self.id)
        self.storage.remove(self.id + '.json')
