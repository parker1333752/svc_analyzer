from DataTable import TxDataTable
from TiDataSet import TiDataSet
class TxDataSet(TiDataSet):
    def __init__(self, id_ , config , nodes):
        self.nodes = nodes
        self.config = config

        if type(id_) == type(u'') or type(id_) == type(b''):
            self.node = self.nodes.get(id_)
            if not self.node:
                self.node = self.nodes.newItem(id_)

        elif type(id_) == type(self.nodes.newItem()):
            self.node = id_

        else:
            raise AssertionError, 'type of id no match <unicode>'

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
        pass

    def newId(self):
        id_ = str(uuid.uuid1()).replace('-','')
        return id_

    def get(self, id_):
        if id_ in self.node.children:
            node = self.nodes.get(id_)

            if node:
                return TxDataTable(node, self.nodes)

    def set(self, id_ , table):
        table.node.ssid = self.config['datatableSsid']
        self.nodes.set(id_, table.node)

    def add(self, table):
        if not table.node.id:
            table.node.id = self.newId()

        table.node.ssid = self.config['datatableSsid']

        self.node.addChildren(table.node.id)
        table.node.addParent(self.node.id)

        self.nodes.add(table.node)

    def remove(self, id_):
        if not id_ in self.node.children:
            return

        self.node.removeChildren(id_)
        self.nodes.remove(id_)

    @property
    def descriptor(self):
        return self.node.properties['descriptor']

    @descriptor.setter
    def descriptor(self, desc):
        self.node.properties['descriptor'] = desc

