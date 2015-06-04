from DataTable import TxDataTable
from TiDataSet import TiDataSet
import uuid

class TxDataSet(TiDataSet):
    def __init__(self, dss, config , nodes):
        self.nodes = nodes
        self.config = config
        self.dss = dss

    def find(self):
        lst = []

        if self.children:
            for i in self.children:
                node = self.nodes.get(i)
                if node:
                    lst.append(node)

        if lst:
            return lst

    def newItem(self, id_ = None):
        '''Create a new datatable object (TxDataTable)
        '''
        if id_ == None:
            id_ = self.newId()

        if id_ and self.nodes.get(id_):
            raise AssertionError, 'This id has been used'

        datatable = TxDataTable(self.config, self.nodes)
        datatable.node = self.nodes.newItem()
        datatable.id = id_
        return datatable

    def newId(self):
        '''Create a new id as dataset_id.
        override it to change the way id generated.
        '''
        id_ = str(uuid.uuid1()).replace('-','')
        return id_

    def get(self, id_):
        if self.node.children and id_ in self.node.children:
            node = self.nodes.get(id_)

            if node:
                datatable = TxDataTable(self.config, self.nodes)
                datatable.node = node
                return datatable

    def set(self, id_ , table):
        if self.node.children and id_ in self.node.children:
            table.node.ssid = self.config['datatableSsid']
            self.nodes.set(id_, table.node)

    def add(self, table):
        if not table.node.id:
            table.node.id = self.newId()

        table.node.ssid = self.config['datatableSsid']

        self.node.addChildren(table.node.id)
        table.node.addParent(self.node.id)

        self.dss.set(self.id, self)
        self.nodes.add(table.node)

    def remove(self, id_):
        if not id_ in self.node.children:
            return

        self.node.removeChildren(id_)
        self.dss.set(self.id, self)
        self.nodes.remove(id_)

    @property
    def id(self):
        return self.node.id

    @id.setter
    def id(self, id_):
        self.node.id = id_

    @property
    def descriptor(self):
        try:
            value = self.node
        except:
            return {}

        if self.node.properties == None:
            self.node.properties = {}

        if self.node.properties.get('descriptor') == None:
            self.node.properties['descriptor'] = {}

        return self.node.properties['descriptor']

    @descriptor.setter
    def descriptor(self, desc):
        if self.node.properties == None:
            self.node.properties = {}

        self.node.properties['descriptor'] = desc

