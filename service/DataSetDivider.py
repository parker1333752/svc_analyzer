from foundation.AppService import TxAppService
from foundation.PostgreAccess import TxPostgreAccess
from foundation.PostgreAccess import PostgreUtils as utils
from struct import pack

class TxDataSetDivider(object):

    def __init__(self, flt):
        self.filter = flt
        self.apps = TxAppService()
        self.ps = self.apps.getPostgreAccess()
        self.dss = self.apps.getDatasets()

    def divide(self):
        dict_data = self.getRawDataFrame()
        if not dict_data or not len(dict_data):
            raise AssertionError, 'No rawdataframe satisfied this query condiction: %s'%self.filter

        test = self.ps.select('task','where id = %s',(self.filter['testid'],))
        if not test or not len(test):
            raise AssertionError, 'No test match this query condiction: %s'%self.filter

        dataset = self.dss.newItem()
        self.dss.add(dataset)
        datatable = dataset.newItem()
        dataset.add(datatable)
        self.ps.update('task',{'nodeid':'%s'%dataset.id},'where id = %s',(self.filter['testid'],))

        for i in dict_data:
            #print len(self.createFileFrame(i))
            datatable.append(self.createFileFrame(i))


    def getRawDataFrame(self):
        begin_datetime = utils.timestamp2datetime(self.filter['begintime'])
        end_datetime = utils.timestamp2datetime(self.filter['endtime'])
        # print begin_datetime
        # print end_datetime
        # print '<%s>'%self.filter['loggerid']
        
        sql = 'where time0 >= %s and time0 < %s and deviceid =%s order by time0,timeoffset'
        return self.ps.select('rawdataframe', sql ,(begin_datetime,end_datetime,self.filter['loggerid']))

    def createFileFrame(self, r):
        # raw data frame columns: ['data', 'altitude', 'time0', 'longitude', 'latitude', 'state', 'deviceid', 'timeoffset', 'type', 'id']
        # file frame format : [Type 1B] [Timestamp 10B] [Longitude 8B] [Latitude 8B] [Altitude 8B] [Device Identifier 1B] [data nB]
        #m_format = 'bqh3db'
        data = b''
        data += pack('b', r['type'])
        data += pack('q', utils.datetime2timestamp(r['time0']))
        data += pack('h', r['timeoffset'])
        data += pack('3d',r['longitude'],r['latitude'],r['altitude'])
        data += pack('b',r['deviceid']%128)
        data += str(r['data'])
        return data

if __name__ == '__main__':
    #['data', 'altitude', 'time0', 'longitude', 'latitude', 'state', 'deviceid', 'timeoffset', 'type', 'id']

    import time
    end = time.time() * 1000
    begin = end - 3600*24*5*1000

    flt = {'begintime':begin,'endtime':end,'loggerid':151513,u'testid':264}
    a = TxDataSetDivider(flt)
    a.divide()

    '''
    apps = TxAppService()
    ps = apps.getPostgreAccess()
    dss = apps.getDatasets()
    nodeid = ps.select('task','where id = %s',(264,))[0]['nodeid']
    dataset = dss.get(nodeid)
    datatable_ids = dataset.node.children
    datatable = dataset.get(datatable_ids[0])
    print datatable.frameLength
    print datatable.rowCount
    print len(datatable.select(1,2)[0])
    '''

    #dataset = dss.pirnt

