import os
from Algorithm import TxAlgorithm
class TxAnalyticalFlow(object):

    def __init__(self):
        self.id = 0
        self.code = ''
        self.note = ''
        self.templateId = 0

        self.inputs = []
        self.outputs = []
        self.algorithms = []
        self.objectstate='waiting' # 'runing', 'finished'

    def run(self):
        print '---------------- flow start (%r)----------------'%id(self)
        print self.__str__()
        for algorithm_name in self.algorithms:
            self.inputs=self.outputs
            algorithm=TxAlgorithm(algorithm_name)
            self.outputs=algorithm.execute(self.inputs)

        print '---------------- flow end (%r)  ----------------'%id(self)

    def propNames(self):
        return ['id', 'code', 'note', 'templateId']

    def getProps(self):
        res, props = {}, self.propNames()

        for k in props:
            res[k] = getattr(self, props)

    def setProps(self, data):
        props = self.propNames()

        for p in props:
            p in data and setattr(self, p, data[p])

        for p in ['inputs', 'outputs', 'algorithms']:
            if p not in data:
                continue
                
            v = getattr(self, p)
            del v[:]
            if type(data[p]) is str:
                v.append(data[p])

            if type(data[p]) is list:
                for item in data[p]:
                    v.append(item)

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        return 'id=%s, code=%s, note=%s, tplid=%s, inputs=%r, output=%r, algorithms=%r.'%(self.id,self.code,self.note,self.templateId,self.inputs,self.outputs,self.algorithms)
