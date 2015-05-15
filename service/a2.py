from foundation import Apps
id_ = '9d9d971af9fb11e48123d4ae52cc5a07'

apps = Apps()
nodes = apps.fdb.getNodes()
data = nodes.load(id_)
print 'data,',data
