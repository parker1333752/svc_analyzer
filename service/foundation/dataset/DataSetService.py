from DataSet import TxDataSet
from TiDataSetService import TiDataSetService

class TxDataSetService(TiDataSetService):
    def __init__(self, config, nodes):
        self.config = config
        self.nodes = nodes

    def find(self, filter_):
        filter_.update({'ssid':self.config['datasetSsid']})
        allDataSetNodes = self.nodes.find(filter_)
        allDataSets = [ TxDataSet(x,config, self.nodes) for x in allDataSetNodes ]
        return allDataSets

    def newItem(self,id_ = None):
        if id_ == None:
            id_ = self.newId()

        if id_ and self.nodes.get(id_):
            raise AssertionError, 'This id has been used'

        return TxDataSet(id_,config,  self.nodes)

    def newId(self):
        id_ = str(uuid.uuid1()).replace('-','')
        return id_

    def get(self, id_):
        node = self.nodes.get(id_)
        if node:
            return TxDataSet(node,config, self.nodes)

    def set(self, id_ , dataset):
        dataset.node.ssid = self.config['datasetSsid']
        self.nodes.set(id_, dataset.node)

    def add(self, dataset):
        node = dataset.node
        if not node.id:
            node.id = self.newId()

        node.ssid = self.config['datasetSsid']

        dataset.node = node
        return self.nodes.add(dataset.node)

    def remove(self, id_):
        self.nodes.iterremove(id_)

