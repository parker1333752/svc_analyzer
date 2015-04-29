import time, config
from multiprocessing import Process

from HttpIoService import TxHttpIoService
from AnalyticalScheduler import TxAnalyticalScheduler

from AnalyticalFlow import TxAnalyticalFlow

class TxAppService():

    def __init__(self, config):
        self.scheduler = TxAnalyticalScheduler()
        self.isRunning = False
        self.httpio = TxHttpIoService(config.serverConfig)
        TxHttpIoService.appService=self

    def interprete(self, data, expecttime = 0):
        flow = TxAnalyticalFlow()
        flow.setProps(data)

        self.scheduler.start(flow,expecttime)

    def startup(self):
        if self.isRunning:
            return False

        try:
            self.httpio.startup()
        except Exception:
            print 'httpIoService startup error'
        self.isRunning = True

    def shutdown(self):
        self.scheduler.shutdown()

    def restart(self):
        self.scheduler.shutdown()
