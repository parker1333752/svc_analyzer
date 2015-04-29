import httplib
from json import *
import urllib
import sys
import time

def printf(f,data):
    old=sys.stdout
    sys.stdout=f
    print data
    sys.stdout=old
    return

url='http://openwsn.tongji.edu.cn/site/mvc/tests'
conn=httplib.HTTPConnection('openwsn.tongji.edu.cn')

# send GET request
#conn.request(method='GET',url=url)
#response=conn.getresponse()
#res=response.read()
#print res

#f=open('data.dat','r')
#requestdata=f.read()
#print requestdata
#print type(requestdata)
#requestdata=JSONDecoder().decode(requestdata)
#print requestdata
#print type(requestdata)
#f.close()
print '---end---'

# send POST request
#header={'Content-Type':'application/json'}
#conn.request(method='POST',url=url,body=requestdata,headers=header)
#response=conn.getresponse()
#res=response.read()
#print res

# send POST with form data as body
#host='192.168.1.151:8000'
#url='http://192.168.1.151:8000/tasks'
#conn=httplib.HTTPConnection(host)
#print url
#data={'id':1,'code':'abcde','note':'hello','templateId':129}
#encodedata=urllib.urlencode(data)
#header={'Content-Type':'application/x-www-form-urlencoded'}
#conn.request(method='POST',url=url,body=encodedata,headers=header)
#response=conn.getresponse()
#res=response.read()
#print res

host='192.168.1.151:8000'
url='http://192.168.1.151:8000/tasks'
conn=httplib.HTTPConnection(host)
print url
data={'id':1,'code':'abcde','note':'hello','templateId':129}
encodedata=urllib.urlencode(data)
header={'Content-Type':'application/x-www-form-urlencoded'}
conn.request(method='POST',url=url,body=encodedata,headers=header)
response=conn.getresponse()
res=response.read()
print res
print type(res)
