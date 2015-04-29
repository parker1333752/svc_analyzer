import time
import os
from AnalyticalFlowService import TxAnalyticalFlowService
#from multiprocessing import Process
from threading import Thread
from threading import Lock
from utils import TimeQueue

class TxAnalyticalScheduler(object):

    def __init__(self):
        self.flows = TxAnalyticalFlowService()
        self.queue = TimeQueue()
        #self.flowMap = {}
        self.mainThread = None
        self.running = None
        self.queuelock=Lock()

    def start(self, flow, expecttime = 0):
        flow = self.flows.add(flow)

        if not flow:
            return False
        print 'added a flow',flow

        self.queuelock.acquire()
        self.queue.add(flow, expecttime)
        self.queuelock.release()

        if self.mainThread==None or self.mainThread.isAlive()==False:
            self.mainThread=Thread(target=self.run)
            self.mainThread.start()

    def run(self):
        print 'scheduler run'
        print '------------------------hello scheduler run--------------------------------------\n'

        while True:
            try:
                lefttime = self.queue.lefttime()
                if not lefttime:
                    self.queuelock.acquire()
                    self.running = self.queue.pop()
                    self.queuelock.release()
                    if self.running:
                        self.running.run()
                else:
                    time.sleep(lefttime)
            except Exception as e:
                print '------------------------scheduler error------------------------------------------\n'
                print e
                break
            finally:
                pass

        self.running = None
        print '------------------------ end scheduler-------------------------------------------\n'

    def shutdown(self):
        pass

    def kill_running(self):
        pass
        # if self.mainThread:
        #     self.mainThread.terminate()
        #     self.mainThread=Thread(target=self.run,args=('subThread',))
        #     self.mainThread.start()

    def getWaitingList(self):
        return [x.to_dict() for x in self.queue.getQueue()]

    def getFlowById(self, id):
        return self.flows.get(id)

    def getAllFlows(self):
        return [x.to_dict() for x in self.flows.getAll().itervalues()]
