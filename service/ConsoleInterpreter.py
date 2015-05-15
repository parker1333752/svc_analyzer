from threading import Thread,Lock
from multiprocessing import Process, Queue
from foundation.RestClient import TxHttpClient
import sys
import os
import time

class _WrapperStdout(object):
    ''' wrapper class of stdout,
    used to get stdout
    '''
    def __init__(self,send_data):
        self.buff = ''
        self.send_data = send_data

    def write(self, data):
        self.buff += data

        ss = self.buff.split('\n')
        self.buff = ss.pop()
        for i in ss:
            self.send_data(i)

        if self.buff == '... ':
            self.send_data(self.buff)
            self.buff = ''

    def flush(self):
        self.send_data(self.buff)
        self.buff = ''

class _TxConsoleModel(object):
    '''console Model
    Only used in TxConsoleInterpreter.
    Storage some information about console process.
    1:1 with console process.
    '''
    consts = ['cmdQueue','ctrlQueue','process']
    def __init__(self):
        self.cmdQueue = Queue()
        #self.ctrlQueue = Queue()
        self.process = None
        self.freshTime = time.time()

    def __setattr__(self, name, value):
        if name in _TxConsoleModel.consts and name in self.__dict__.keys():
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
        # how many subprocess can be run in the same time.
        'MAX_PROCESS_COUNT' : 10,
        # if not any cmd input over this time,subprocess will be closed.
        'TERMINATE_TIMEOUT' : 3600, 
        # just for display
        'CONSOLES_FILENAME' : '<myconsole>', 
    }

    def __init__(self):
        self.consoles = {}
        #self.pool = None
        #self.manager = None
        self.consolesLock = Lock()
        self.cmdBuffer = []
        self.cmdBufferLock = Lock()
        self.cmdscannerThread = None
        self.started = False
        self.__register_terminal()

    def start(self):
        print 'console pool start',os.getpid()
        self.started = True
        Thread(target=self.garbage_collection).start()

    def is_started(self):
        return self.started

    def __del__(self):
        self.terminate()

    def __register_terminal(self):
        def getfunc(origin):
            def func(sig,frame):
                self.terminate()
                origin(sig,frame)
            return func

        import signal
        func1 = getfunc(signal.getsignal(signal.SIGINT))
        func2 = getfunc(signal.getsignal(signal.SIGTERM))
        signal.signal(signal.SIGINT,func1)
        signal.signal(signal.SIGTERM,func2)

    def terminate(self):
        '''
        close Process pool
        close result scanner
        '''
        self.started = False
        print 'doing something closing'

        for i in self.consoles.keys():
            self._delete_console(i)

    def input_cmd(self,consoleId=None,cmd=''):
        self.cmdBufferLock.acquire()
        args = (consoleId,cmd)
        self.cmdBuffer.append(args)
        self.cmdBufferLock.release()

        if self.cmdscannerThread == None or not self.cmdscannerThread.is_alive():
            self.cmdscannerThread = Thread(target=self.cmd_scanner)
            self.cmdscannerThread.start()


    def cmd_scanner(self):
        '''scan for cmd input'''
        while self.started:
            if len(self.cmdBuffer) > 0:
                self.cmdBufferLock.acquire()
                item = self.cmdBuffer.pop(0)
                self.cmdBufferLock.release()

                print 'id=<%s>, cmd=<%s>. count=%d'%(item[0],item[1],len(self.consoles))

                if item[1] == 'clear':
                    print self._delete_console(item[0])

                else:
                    print self._add_console(item[0])

                    if item[1] != None:
                        self._push_input(item[0],item[1])
                    else:
                        self._push_input(item[0])

            else:
                break

    def garbage_collection(self):
        while self.started:
            nowTime = time.time()
            garbageList = []
            self.consolesLock.acquire()
            for i in self.consoles.iterkeys():
                console = self.consoles[i]
                if console.freshTime + TxConsoleInterpreter.config['TERMINATE_TIMEOUT'] <= nowTime:
                    garbageList.append(i)

            self.consolesLock.release()
            for i in garbageList:
                self._delete_console(i)

            time.sleep(10)

    def has_console(self,consoleId=None):
        self.consolesLock.acquire()
        if self.consoles.has_key(consoleId):
            rt = True
        else:
            rt = False
        self.consolesLock.release()
        return rt

    def _add_console(self,consoleId=None):
        if self.started == False:
            return 'console pool haven\'t start'

        self.consolesLock.acquire()
        if self.consoles.has_key(consoleId):
            self.consolesLock.release()
            return 'id existed'

        if len(self.consoles) >= TxConsoleInterpreter.config['MAX_PROCESS_COUNT']:
            self.consolesLock.release()
            return 'Process pool is full'

        console = _TxConsoleModel()
        #args = (console.cmdQueue,console.ctrlQueue,consoleId)
        args = (console.cmdQueue,consoleId)
        #console.result = self.pool.apply_async(console_process,args=args)
        console.process = Process(target=console_process,args=args)
        console.close_handler = Thread(target=self._close_handler,args=(consoleId,console.process))

        self.consoles[consoleId] = console

        console.close_handler.start()
        self.consolesLock.release()

        return 'add new console: %s'%consoleId

    def _close_handler(self,consoleId,mprocess):

        mprocess.start()
        mprocess.join()

        del self.consoles[consoleId]

        print 'proces close,',consoleId

    def _delete_console(self,consoleId=None):
        '''
        delete a console process
        '''
        print 'delete1',consoleId
        self.consolesLock.acquire()
        console = self.consoles.get(consoleId)
        self.consolesLock.release()

        if console == None:
            return 'there is not such console'
        else:
            console.process.terminate()

    def _fetch_output(self,consoleId=None):
        '''
        read output buffer and clear it
        '''
        if not self.consoles.has_key(consoleId) or self.consoles[consoleId].result.ready():
            return
        
        data = ''
        while not self.consoles[consoleId].outputQueue.empty():
            data += self.consoles[consoleId].outputQueue.get()
        
        if len(data) == 0:
            data = None

        return data

    def _push_input(self,consoleId=None,data=''):
        '''
        write a command to input queue
        console process will read from input queue to get python command
        '''
        if data == None:
            return

        self.consolesLock.acquire()
        if not self.consoles.has_key(consoleId):
            self.consolesLock.release()
            return 'there is not such console'

        self.consoles[consoleId].cmdQueue.put(data)
        self.consolesLock.release()

def console_process(cmdQueue,consoleId):
    '''
    Read command from stdin
    and execute command,
    write console output to stdout.
    '''
    print 'subprocess start,',os.getpid()

    import code
    from config import AlgorithmFolder as workFolder
    os.chdir(workFolder)

    from config import consoleConfig as globalConfig
    client = TxHttpClient()
    client.connect(globalConfig['remote_host'],globalConfig['remote_port'])

    def __send_data(data):
        if data == None:
            return
        client.post(globalConfig['remote_path']+'?uuid=%s'%consoleId,data)

    wrapperStdout = _WrapperStdout(__send_data)
    __console_out__ = sys.stdout
    __console_err__ = sys.stderr
    sys.stdout = wrapperStdout
    sys.stderr = wrapperStdout

    def readline(a):
        if a != '>>> ':
            sys.stdout.write(a)

        cmd = cmdQueue.get()
        return cmd

    code.interact('',readline)

    sys.stdout = __console_out__
    sys.stderr = __console_err__
    print 'subprocess closed,',os.getpid()
    return 0

