import httplib
from urlparse import urlparse
class TxHttpClient(object):
    '''
    simple model of http client,
    for http request.
    run connect() before send request.
    '''
    def __init__(self):
        self.conn = None
        self.host = None

    def connect(self,url='localhost'):
        urlObject = urlparse(url)

        if not urlObject.hostname or urlObject.hostname == self.host:
            return

        if urlObject.scheme != 'http':
            raise AssertionError, 'not http request'

        self.close()
        self.host = urlObject.hostname
        self.conn = httplib.HTTPConnection(urlObject.hostname,port)

    def close(self):
        self.conn.close()
        self.conn = None
        self.host = None

    def get(self,url):
        self.connect(url)

        self.conn.request('GET',url)
        response = self.conn.getresponse()
        rdata = response.read()

        return rdata

    def post(self,url,data=None,headers={}):
        self.connect(url)

        self.conn.request('POST',url,data,headers)
        response = self.conn.getresponse()
        rdata = response.read()

        return rdata

    def put(self,url,data=None,headers={}):
        self.connect(url)

        self.conn.request('PUT',url,data,headers)
        response = self.conn.getresponse()
        rdata = response.read()

        return rdata

    def delete(self,url,data=None,headers={}):
        self.connect(url)

        self.conn.request('DELETE',url,data,headers)
        response = self.conn.getresponse()
        rdata = response.read()

        return rdata
