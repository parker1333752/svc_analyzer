from foundation import Apps
apps = Apps()


nodes = apps.getFdb().getNodes()
node = nodes.newItem('rawdatafiles','123123123')

myProperties = {'hello':'I','am':1}
node.saveProperties(myProperties)

properties = node.loadProperties()
print properties

mfile = node.getFile()
mfile.save('hello')

data = mfile.load()
print data
