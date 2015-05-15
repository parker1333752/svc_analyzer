#import httplib
#conn = httplib.HTTPConnection('192.168.1.153',27017)
#conn.request('GET','/')
#response = conn.getresponse()
#data = response.read()
#print data
from pymongo import MongoClient

mon = MongoClient('192.168.1.153',27017)
a = mon.test
print a
