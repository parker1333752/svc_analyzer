import os

class TxRawStorageFile(object):
    def __init__(self,filepath = None):
        self.filepath = filepath
        self.length = None # =None, file is closed; else file is opened
        #self.type = 'file'

    def open(self):
        if self.__dict__.has_key('fd') and self.fd:
            self.fd.close()

        try:
            self.fd = open(self.filepath,'rb+',0)
            self.length = os.path.getsize(self.filepath)
        except:
            fd = open(self.filepath,'w')
            fd.close()
            self.fd = open(self.filepath,'rb+',0)
            self.length = 0

    def close(self):
        if self.fd:
            self.fd.close()
            self.length = None
            del self.fd

    def seek(self,offset = 0):
        '''need to call open() first'''
        return self.fd.seek(offset,0)

    def tell(self):
        '''get current file position,
        need to call open() first
        '''
        return self.fd.tell()

    def read(self, size = 0):
        '''need to call open() first'''
        return self.fd.read(size)

    def readline(self):
        '''need to call open() first'''
        data = self.fd.readline()
        if data:
            return data.replace('\n','').replace('\r','')
        else:
            raise AssertionError, 'end of file'

    def write(self,data):
        '''need to call open() first'''
        self.fd.write(data)

    def append(self,data):
        fd = open(self.filepath,'ab')
        fd.write(data)
        fd.close()

    def load(self):
        self.open()

        data = self.read(self.length)
        self.close()
        return data

    def save(self,data):
        fd = open(self.filepath,'wb')
        fd.write(data)
        fd.close()
