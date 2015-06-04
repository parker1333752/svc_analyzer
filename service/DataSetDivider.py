from foundation.AppService import TxAppService
from foundation.PostgreAccess import TxPostgreAccess
from foundation.PostgreAccess import PostgreUtils as utils

class TxDataSetDivider(object):

    def __init__(self, flt):
        self.filter = flt
        self.apps = TxAppService()
        self.ps = self.apps.getPostgreAccess()

    def divide(self):
        dict_data = getRawDataFrame()
        print [x.iterkeys() for x in dict_data]

    def getRawDataFrame(self):
        #, self.filter['loggerid'])
        begin_datetime = utils.timestamp2datetime(self.filter['begintime'])
        end_datetime = utils.timestamp2datetime(self.filter['endtime'])
        print begin_datetime
        print end_datetime
        
        sql = 'where time0 >= %s and time0 < %s and deviceid =%s order by time0,timeoffset limit 30'
        return self.ps.select('rawdataframe', sql ,(begin_datetime,end_datetime,self.filter['loggerid']))

    def createFileFrame(self, rdf):
        pass

if __name__ == '__main__':
    import time
    end = time.time() * 1000
    begin = end - 3600*24*5*1000

    flt = {'begintime':begin,'endtime':end,'loggerid':151513}
    a = TxDataSetDivider(flt)
    print a.getRawDataFrame()[0].keys()
