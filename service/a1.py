from threading import Thread
from multiprocessing import Process
import time

class abc(object):
    def __init__(self):
        self.a = 1

    def printf(self,abc):
        print 'hello',self.a+abc
        self.a += 1

    def run(self):
        while True:
            print 'hello'
            time.sleep(1)

    def start(self):
        self.process = Process(target=self.run)
        self.process.start()
        Thread(target=self.scan).start()
        self.on_delete()

    def scan(self):
        rt = None
        try:
            #print dir(self.process)
            rt = self.process.join()
        except Exception as e:
            print 'scan error',e

        print 'returncode =',rt

    def stop(self):
        self.process.terminate()

    def on_delete(self):
        def getfunc(origin):
            def func(sig,frame):
                self.stop()
                print 'end of abc'
                print sig
                origin(sig,frame)
            return func
        import signal
        func1 = getfunc(signal.getsignal(signal.SIGINT))
        func2 = getfunc(signal.getsignal(signal.SIGTERM))
        signal.signal(signal.SIGINT,func1)
        signal.signal(signal.SIGTERM,func2)

a = abc()
a.start()
time.sleep(4)
a.stop()

try:
    while True:
        print 'hello'
        time.sleep(1)
except:
    print 'endofexcept'

