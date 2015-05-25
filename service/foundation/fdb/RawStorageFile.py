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

    def read(self, size = 0):
        try:
            return self.fd.read(size)
        except:
            raise AssertionError, 'file havn\'t opened, need to call %s.open() first'%self.__class__.__name__

    def readline(self):
        data = self.fd.readline()
        if data:
            return data.replace('\n','').replace('\r','')
        else:
            raise AssertionError, 'end of file'

    def write(self,data):
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
