import json
import os

f = open('jsontest','r+')
length = os.path.getsize('jsontest')
data = f.read(length)
print repr(data)
print data
print 1
f.close()


#print data
#f.write('lsj')
#f.seek(0,0)
#f.write('lsj')
#f.close()
