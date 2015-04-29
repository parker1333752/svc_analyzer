from AnalyticalFlow import TxAnalyticalFlow

class TxAnalyticalFlowService():

    def __init__(self):
        self.flows = {}

    def add(self, flow):
        if isinstance(flow, TxAnalyticalFlow):
            if not self.flows.has_key(str(flow.id)):
                self.flows[str(flow.id)] = flow
                return flow

    def remove(self, id):
        if str(id) in self.flows:
            self.flows.pop(str(id))

    def get(self, id):
        a = str(id) in self.flows and self.flows[str(id)] or None
        if a !=None:
            # return a.__str__()
            return a.to_dict()
        else:
            return None

    def getAll(self):
        return self.flows
