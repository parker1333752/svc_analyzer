from TiDataTable import TiDataTable
from struct import pack
import uuid
import json

class TxDataTable(TiDataTable):
    def __init__(self, config,  nodes):
        self.config = config
        self.nodes = nodes

        # Record line start position,
        # used to improve reading speed.
        self.__filepos = {0:0}

    def _select_binary(self, rowstart, rowend):
        fd = self.nodes.getFile(self.node.id)
        fd.open()

        frameLength = self.frameLength
        rowcount = self.rowCount

        if rowstart >= rowcount:
            return None
        if rowend > rowcount:
            rowend = rowcount

        fd.seek(frameLength * rowstart)
        rt = []
        for i in range(rowstart,rowend):
            data = fd.read(frameLength)
            rt.append(data)

        fd.close()
        return rt

    def _select_ascii(self, rowstart, rowend):
        last_row = self.__find_maxOfless(self.__filepos.iterkeys(), rowstart)

        fd.open()
        fd.seek(self.__filepos[last_row])

        for i in range(last_row,rowstart):
            data = fd.readline()
            if data:
                self.__filepos[i+1] = fd.tell()
            else:
                break

        rt = []
        for i in range(rowstart,rowend):
            data = fd.readline()
            if data:
                self.__filepos[i+1] = fd.tell()
                try:
                    rt.append(json.loads(data))
                except:
                    pass

            else:
                break

        fd.close()
        return rt

    def select(self, rowstart , rowend):
        '''row index start from 0,
        return data from rowstart (include) to rowend (exclude)
        '''
        if self.descriptor.get('dataformat') == 'ascii':
            return self._select_ascii(rowstart, rowend)

        #elif self.descriptor['dataformat'] == 'binary':
        '''set as default mode : binary'''
        return self._select_binary(rowstart, rowend)

    def append(self, data):
        if type(data) == type([]):
            temp = data
            data = ''
            for i in temp:
                if len(i) <  self.frameLength:
                    i += (self.frameLength - len(i))*pack('b',0)
                data = ''.join([data, i[:self.frameLength]])

        elif type(data) == type(b''):
            mod = len(data) % self.frameLength
            if mod:
                data += (self.frameLength - mod)*pack('b',0)

        else:
            raise AssertionError, 'Type of data if invalid'

        fd = self.nodes.getFile(self.node.id)
        fd.open()
        fd.append(data)
        fd.close()

    @staticmethod
    def __find_maxOfless(iterdata, maxdata):
        '''find max line index in iterdata,
        result also need to less than maxdata
        '''
        linelst = sorted(iterdata)

        l = 0
        r = len(linelst) - 1
        m = None
        while r > l + 1:
            m = (r + l)/2
            if linelst[m] > maxdata:
                r = m - 1
            elif linelst[m] < maxdata:
                l = m
            else:
                break

        if linelst[r] <= maxdata:
            return linelst[r]
        else:
            return linelst[l]

    @property
    def rowCount(self):
        '''Only used in binary format file'''
        try:
            rt = self.__rowCount
        except:
            frameLength = self.frameLength

            fd = self.nodes.getFile(self.node.id)
            filelen = fd.length
            if not fd.length:
                fd.open()
                filelen = fd.length
                fd.close()

            rowcount = filelen / frameLength
            return rowcount

    #@property
    #def frameLength(self):
        #'''Only used in binary format file'''
        #try:
            #rt = self.__frameLength
        #except:
            ## length = 0
            ## for i in self.descriptor['columns']:
                ## length += i['size']

            #fd = self.nodes.getFile(self.node.id)
            #fd.open()
            #a = fd.read(2)

            #import struct
            #try:
                #length = struct.unpack('h',a)
            #except:
                #raise AssertionError, 'File not exists'
            #finally:
                #fd.close()

            #self.__frameLength = length
        #return self.__frameLength

    @property
    def frameLength(self):
        '''Only used in binary format file'''
        try:
            rt = self.__frameLength
        except:
            self.__frameLength = self.config['frameLength']

        return self.__frameLength

    @property
    def id(self):
        return self.node.id

    @id.setter
    def id(self, id_):
        self.node.id = id_

    @property
    def descriptor(self):
        try:
            value = self.node
        except:
            return {}

        if self.node.properties == None:
            self.node.properties = {}

        if self.node.properties.get('descriptor') == None:
            self.node.properties['descriptor'] = {}

        return self.node.properties['descriptor']

    @descriptor.setter
    def descriptor(self, desc):
        if self.node.properties == None:
            self.node.properties = {}

        self.node.properties['descriptor'] = desc

