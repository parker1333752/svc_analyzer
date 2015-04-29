# coding=gbk
'''
Created on 2015年3月5日

@author: wenhan
'''
import struct

fin = open('C:/Users/wenhan/Desktop/Data Analysis/201401242246500.alog',"rb")
fout = open('C:/Users/wenhan/Desktop/Data Analysis/data.txt',"w")

data=[1,1,1,1.1,1,1,1,1,1,1,1,1,1,1,1]
try:
    unusebyte=fin.read(16)
    for list in range(1,18000):
        byte=fin.read(26)
        ai=struct.unpack('26B',byte)
        data[0]=(ai[18]+ai[19]*256+ai[20]*256**2+ai[21]*256**3+ai[22]*256**4+ai[23]*256**5+ai[24]*256**6+ai[25]*256**7)*0.000001
        data[0]=round(data[0],6)
        data[1]=ai[0]
        data[2]=ai[6]+ai[7]*256
        data[3]=ai[1]
        data[4]=ai[2]
        data[5]=ai[4]
        data[6]=ai[3]
        data[7]=ai[10]
        data[8]=ai[11]
        data[9]=ai[12]
        data[10]=ai[13]
        data[11]=ai[14]
        data[12]=ai[15]
        data[13]=ai[16]
        data[14]=ai[17]
        fout.write("%s\n"%data)
    print('success!')
finally:
    fin.close()
