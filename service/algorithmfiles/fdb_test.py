from foundation import Apps
apps = Apps()

# get node service
nodes = apps.getFdb().getNodes()

# create a node object.
# every node is only assigned by ssid and node's id.
node = nodes.newItem('rawdatafiles','123123123')

# edit a new dict data, and save it as node properties.
myProperties = {'hello':'I','am':1}
node.saveProperties(myProperties)

# load node protpert
properties = node.loadProperties()
print properties

# save file data
mfile = node.getFile()
mfile.save('hello')

# load file data
data = mfile.load()
print data

# copy node, format: copy(dest,src)
node2 = nodes.newItem('rawdatafiles2','123123123')
nodes.copy(node2,node)

# remove node and file
node.remove()

# read node file as binary string
mfile = node2.getFile()
mfile.open()
print 'length =',mfile.length
try:
    while True:
        a = mfile.read(1)
        if not a:
            break
        print '<%s>'%a
except Exception as e:
    print 'error :',e
