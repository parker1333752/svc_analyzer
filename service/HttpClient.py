import httplib
class TxHttpClient(object):
    '''
    simple model of http client,
    for http request.
    run connect() before send request.
    '''
    def __init__(self):
        self.conn = None

    def connect(self,host='localhost',port=80):
        self.conn = httplib.HTTPConnection(host,port)

    def get(self,path=''):
        self.conn.request('GET',self.baseurl+path)
        response = self.conn.getresponse()
        rdata = response.read()
        return rdata

    def post(self,url='',data=None,headers={}):
        self.conn.request('POST',url,data,headers)
        response = self.conn.getresponse()
        rdata = response.read()
        return rdata

    def put(self,url='',data=None,headers={}):
        self.conn.request('PUT',url,data,headers)
        response = self.conn.getresponse()
        rdata = response.read()
        return rdata

    def delete(self,url='',data=None,headers={}):
        self.conn.request('DELETE',url,data,headers)
        response = self.conn.getresponse()
        rdata = response.read()
        return rdata
