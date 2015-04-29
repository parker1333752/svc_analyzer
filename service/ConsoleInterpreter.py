from threading import Thread,Lock
from multiprocessing import Pool, Manager
from HttpClient import TxHttpClient
from config import consoleConfig as globalConfig
import sys
import os
import time

class _WrapperStdout(object):
    ''' wrapper class of stdout,
    used to get stdout
    '''
    def __init__(self,queue):
        self.queue = queue

    def write(self, data):
        self.queue.put(data)

class _TxConsoleModel(object):
    '''console Model
    Only used in TxConsoleInterpreter.
    Storage some information about console process.
    1:1 with console process.
    '''
    consts = ['cmdQueue','outputQueue','ctrlQueue','result']
    def __init__(self,manager):
        self.cmdQueue = manager.Queue()
        self.outputQueue = manager.Queue()
        self.ctrlQueue = manager.Queue()
        self.result = None

    def __setattr__(self, name, value):
        if name in self.__class__.consts and name in self.__dict__.keys():
            if self.__dict__[name] != None:
                pass
            else:
                self.__dict__[name]=value
        else:
            self.__dict__[name]=value

class TxConsoleInterpreter(object):
    ''' console interpreter.
    create new processes to run console, these processes storaged by Pool.
    use http client to send result back.
    '''
    config = {
        'MAX_PROCESS_COUNT' : 10,
        'TERMINATE_TIMEOUT' : 10,
        'CONSOLES_FILENAME' : '<myconsole>', # just for display
    }

    def __init__(self):
        self.consoles = {}
        self.pool = None
        self.manager = None
        self.client = TxHttpClient()
        self.scannerRunning = False
        self.cmdBuffer = []
        self.consolesLock = Lock()
        self.cmdBufferLock = Lock()

    def start(self):
        '''
        start Process Pool,
        create new Thread to run result scanner.
        '''
        print 'console pool start',os.getpid()
        self.pool = Pool(self.__class__.config['MAX_PROCESS_COUNT'])
        self.manager = Manager()
        self.consoles = {}

        self.scannerRunning = True
        self.scannerThread = Thread(target=self.output_scanner)
        self.scannerThread.start()
        self.cmdscannerThread = Thread(target=self.cmd_scanner)
        self.cmdscannerThread.start()

        self.client.connect(globalConfig['remote_host'],globalConfig['remote_port'])

    def is_started(self):
        if self.pool != None:
            return True
        else:
            return False

    def terminate(self):
        '''
        close Process pool
        close result scanner
        '''
        self.scannerRunning = False

        self.consolesLock.aquire()
        for i in self.consoles.itervalues():
            i.ctrlQueue.put(True)
        #self.pool.close()
        self.pool.terminate()
        self.pool = None
        self.consolesLock.release()

    def input_cmd(self,consoleId=None,cmd=''):
        self.cmdBufferLock.acquire()
        args = (consoleId,cmd)
        self.cmdBuffer.append(args)
        self.cmdBufferLock.release()

    def cmd_scanner(self):
        '''scan for cmd input'''
        print 'start scan cmd'
        while self.scannerRunning:
            if not len(self.cmdBuffer) == 0:
                self.cmdBufferLock.acquire()

                for i in self.cmdBuffer:
                    if i[1] == 'clear':
                        print self._delete_console(i[0])

                    else:
                        if not self.has_console(i[0]):
                            print self._add_console(i[0])

                        if i[1] != None:
                            self._push_input(i[0],i[1])
                        else:
                            self._push_input(i[0])

                self.cmdBuffer = []

                self.cmdBufferLock.release()

            time.sleep(0.1)

    def output_scanner(self):
        '''scan console result output, and send it out by Http Client.
        Shall run in new Thread and non-block main Thread
        '''
        print 'start scan result'
        while self.scannerRunning:
            self.consolesLock.acquire()

            for i in self.consoles.iterkeys():
                data = self._fetch_output(i)
                if data != None:
                    self._send_data(i,data)

            self.consolesLock.release()
            
            time.sleep(0.1)

        print 20*'-','console terminate','-'*20

    def has_console(self,consoleId=None):
        self.consolesLock.acquire()
        if self.consoles.has_key(consoleId):
            rt = True
        else:
            rt = False
        self.consolesLock.release()
        return rt

    def _add_console(self,consoleId=None):
        if self.pool == None:
            return 'console process pool haven\'t started'

        self.consolesLock.acquire()
        if self.consoles.has_key(consoleId):
            self.consolesLock.release()
            return 'id existed'

        if len(self.consoles) >= self.__class__.config['MAX_PROCESS_COUNT']:
            self.consolesLock.release()
            return 'Process pool is full'

        console = _TxConsoleModel(self.manager)

        args = (console.cmdQueue,console.outputQueue,console.ctrlQueue)
        console.result = self.pool.apply_async(console_process,args=args)

        self.consoles[consoleId] = console

        self.consolesLock.release()
        return

    def _delete_console(self,consoleId=None):
        '''
        delete a console process
        '''
        self.consolesLock.acquire()
        if not self.consoles.has_key(consoleId):
            self.consolesLock.release()
            return 'there is not such console'

        self.consoles[consoleId].ctrlQueue.put(True)

        try:
            self.consoles[consoleId].result.wait(self.__class__.config['TERMINATE_TIMEOUT'])
        except Exception as e:
            return 'Process can\'t be terminated'
        finally:
            del self.consoles[consoleId]
            self.consolesLock.release()

    def _fetch_output(self,consoleId=None):
        '''
        read output buffer and clear it
        '''
        if not self.consoles.has_key(consoleId) or self.consoles[consoleId].result.ready():
            return
        
        data = ''
        while not self.consoles[consoleId].outputQueue.empty():
            data += self.consoles[consoleId].outputQueue.get()

        #self.consoles[consoleId].outputQueue.task_done()
        
        if len(data) == 0:
            data = None

        return data

    def _push_input(self,consoleId=None,data=None):
        '''
        write a command to input queue
        console process will read from input queue to get python command
        '''
        print 'hello, id=<%s>, cmd=<%s>'%(consoleId,data)
        if data == None:
            return

        self.consolesLock.acquire()
        if not self.consoles.has_key(consoleId):
            self.consolesLock.release()
            return 'there is not such console'

        self.consoles[consoleId].cmdQueue.put(data)
        self.consolesLock.release()

    def _send_data(self,consoleId=None,data=None):
        '''
        use http client to send data to Vert.x verticle.
        Or you can rewrite this method and use other way to send data
        '''
        if data == None:
            return

        print 'send ',data
        self.client.post(globalConfig['remote_path']+'?uuid=%s'%consoleId,data)

def console_process(cmdQueue,outputQueue,ctrlQueue):
    '''
    Read command from stdin
    and execute command,
    write console output to stdout.
    '''
    from config import AlgorithmFolder as workFolder
    os.chdir(workFolder)

    print 'subprocess start,',os.getpid()

    wrapperStdout = _WrapperStdout(outputQueue)
    __console_out__ = sys.stdout
    __console_err__ = sys.stderr
    sys.stdout = wrapperStdout
    sys.stderr = wrapperStdout

    def readline(a):
        sys.stdout.write(a)
        while cmdQueue.empty():
            pass

        cmd = cmdQueue.get()
        print cmd
        return cmd

    import code
    code.interact(None,readline)

    sys.stdout = __console_out__
    sys.stderr = __console_err__
    return 0

