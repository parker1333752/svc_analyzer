from foundation import Apps

apps = Apps()
nodes = apps.getCms().getNodes()

node = nodes.newItem()
print node.id

node.ssid = 'datasetfiles'
nodes.add(node)

id_ = node.id
print id

node1 = nodes.get(id_)
print node1.__dict__

mfile = nodes.getFile(id_)
mfile.save('hello\ntest\ndata\n')
mfile.open()
print mfile.length

lines = []
try:
    mfile.open()
    while True:
        line = mfile.readline()
        print line
        lines.append(line)
except Exception as e:
    print 'start'
    print e
    print 'end'
    print lines
    mfile.close()
    print 'all end'
