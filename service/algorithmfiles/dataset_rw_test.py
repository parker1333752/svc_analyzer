from foundation import Apps

apps = Apps()

dss = apps.getDatasets()
#print dir(dss)

'''
1. dataset operation
'''
'''get all datasets'''
#print dss.find()

'''add a new dataset'''
#dataset = dss.newItem()
#dataset.descriptor = {'hello':'dataset_test'}
#dss.add(dataset)
#print dataset.id
'''The code following is used to record new dataset id, for test reason'''
#f = open('dataset_write_test.py','a')
#f.write('\ndatasetid: %s\n'%dataset.id)
#f.close()
#da16cbea09fe11e5aa02d4ae52cc5a07

'''get an exists dataset'''
#dataset = dss.get('da16cbea09fe11e5aa02d4ae52cc5a07')
#print dataset.id
#print dataset.descriptor
#print dataset.node.__dict__

'''remove an exists dataset'''
#dss.remove('63751d7009fe11e5985ad4ae52cc5a07')

'''update descriptor of exists dataset'''
#dataset = dss.get('da16cbea09fe11e5aa02d4ae52cc5a07')
#dataset.descriptor['1231'] = 123123
#dss.set(dataset.id, dataset)



'''
2. datatable operation
'''
'''create new datatable (in an exists dataset)'''
#dataset = dss.get('da16cbea09fe11e5aa02d4ae52cc5a07')
#datatable = dataset.newItem()
#datatable.descriptor = {'framelength':64}
#dataset.add(datatable)
'''The code following is used to record new datatable id, for test reason'''
#f = open('dataset_write_test.py','a')
#f.write('\ndatatableid: %s\n'%datatable.id)
#f.close()
#datatableid: 257a76c40a9d11e58c46d4ae52cc5a07

'''get an exists datatable (from exists dataset)'''
#dataset = dss.get('da16cbea09fe11e5aa02d4ae52cc5a07')
#print dataset.node.__dict__
#datatable = dataset.get('257a76c40a9d11e58c46d4ae52cc5a07')
#print datatable.node.__dict__

'''remove an exists datatable'''
#dataset = dss.get('da16cbea09fe11e5aa02d4ae52cc5a07')
#dataset.remove('6c37b9720a9911e5a185d4ae52cc5a07')

'''update descriptor of exists datatable'''
#dataset = dss.get('da16cbea09fe11e5aa02d4ae52cc5a07')
#datatable = dataset.get('257a76c40a9d11e58c46d4ae52cc5a07')
#datatable.descriptor['test'] = 'datatable'
#dataset.set(datatable.id, datatable)



'''
3. R/W datatable file
'''
#dataset = dss.get('da16cbea09fe11e5aa02d4ae52cc5a07')
#datatable = dataset.get('257a76c40a9d11e58c46d4ae52cc5a07')
#print datatable.rowCount

'''write to a datatable'''
#from struct import pack
#datatable.append(pack('3h',1,2,3))
#datatable.append(pack('3h',6,5,4))

'''read from a datatable'''
#print datatable.select(0,1)
#print datatable.select(11,12)




'''
4. get datatables from testid
'''
ps = apps.getPostgreAccess()
testid = 264
datasetid = ps.select('task','where id = %s',(testid,))[0]['nodeid']
dataset = dss.get(datasetid)
datatable_ids = dataset.node.children
print datatable_ids
for i in datatable_ids:
    datatable = dataset.get(i)
    print datatable.id
    #data = datatable.select(0,1)
    print len(datatable.select(0,1)[0])
