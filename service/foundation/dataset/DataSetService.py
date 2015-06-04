from DataSet import TxDataSet
from TiDataSetService import TiDataSetService
import uuid

class TxDataSetService(TiDataSetService):
    def __init__(self, config, nodes):
        self.config = config
        self.nodes = nodes

    def find(self, filter_={}):
        filter_.update({'ssid':self.config['datasetSsid']})
        allDataSetNodes = self.nodes.find(filter_)

        def creaate_dataset(node):
            dataset = TxDataSet(self, self.config, self.nodes)
            dataset.node = node
            return dataset

        allDataSets = [ creaate_dataset(x) for x in allDataSetNodes ]
        return allDataSets

    def newItem(self,id_ = None):
        '''Create a new dataset object (TxDataSet).
        '''
        if id_ == None:
            id_ = self.newId()

        if id_ and self.nodes.get(id_):
            raise AssertionError, 'This id has been used'

        dataset = TxDataSet(self, self.config,  self.nodes)
        dataset.node = self.nodes.newItem()
        dataset.id = id_
        return dataset

    def newId(self):
        '''Create a new id as dataset_id.
        override it to change the way id generated.
        '''
        id_ = str(uuid.uuid1()).replace('-','')
        return id_

    def get(self, id_):
        '''Get a dataset (TxDataSet object), and load node information.
        '''
        node = self.nodes.get(id_)
        if node:
            dataset = TxDataSet(self , self.config, self.nodes)
            dataset.node = node
            return dataset

    def set(self, id_ , dataset):
        '''Set dataset descriptor to node.
        '''
        dataset.node.ssid = self.config['datasetSsid']
        self.nodes.set(id_, dataset.node)

    def add(self, dataset):
        '''Add a node in MongoDB to storage dataset information.
        '''
        node = dataset.node
        if not dataset.id:
            dataset.id = self.newId()

        dataset.node.ssid = self.config['datasetSsid']

        return self.nodes.add(dataset.node)

    def remove(self, id_):
        '''Remove dataset (and corresponding node)
        Recursively remove datatable.
        '''
        self.nodes.iterremove(id_)

