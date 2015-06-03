from TiDataTable import TiDataTable
import json

class TxDataTable(TiDataTable):
    def __init__(self, id_, nodes):
        self.nodes = nodes

        if type(id_) == type(u'') or type(id_) == type(b''):
            self.node = self.nodes.get(id_)
            if not self.node:
                self.node = self.nodes.newItem(id_)

        elif type(id_) == type(self.nodes.newItem()):
            self.node = id_

        else:
            raise AssertionError, 'type of id no match <unicode>'

        # Record line start position,
        # for improve reading speed
        self.filepos = {0:0}

    def _select_binary(self, rowstart, rowend):
            fd = self.nodes.getFile(self.node.id)
            fd.open()

            frameLength = self.frameLength
            rowcount = fd.length / frameLength

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
            last_row = self.__find_maxOfless(self.filepos.iterkeys(), rowstart)

            fd = open()
            fd.seek(self.filepos[last_row])

            for i in range(last_row,rowstart):
                data = fd.readline()
                if data:
                    self.filepos[i+1] = fd.tell()
                else:
                    break

            rt = []
            for i in range(rowstart,rowend):
                data = fd.readline()
                if data:
                    self.filepos[i+1] = fd.tell()
                    try:
                        rt.append(json.loads(data))
                    except:
                        pass

                else:
                    break

            return rt

    def select(self, rowstart , rowend):
        '''row index start from 0,
        return data from rowstart (include) to rowend (exclude)
        '''
        if self.descriptor['dataformat'] == 'binary':
            return self._select_binary(rowstart, rowend)

        elif self.descriptor['dataformat'] == 'ascii':
            return self._select_ascii(rowstart, rowend)

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
    def frameLength(self):
        try:
            rt = self.__frameLength
        except:
            length = 0
            for i in self.descriptor['columns']:
                length += i['size']
            self.__frameLength = length

        return self.__frameLength

    @property
    def descriptor(self):
        return self.node.properties['descriptor']

    @descriptor.setter
    def descriptor(self, desc):
        self.node.properties['descriptor'] = desc

