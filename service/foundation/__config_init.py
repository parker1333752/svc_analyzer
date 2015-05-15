import json
import os
a = {'mongohost':'192.168.1.153','mongoport':27017}
mongoNodeStorages = {'RawStorageService':{},'MongoStorageService':{}}
a['cmsStorages'] = mongoNodeStorages
fdbNodeStorages = {'RawStorageService':{'rawdatafiles':'/home/lisijun/svc_storages/rawdata','datasetfiles':'/home/lisijun/svc_storages/dataset'},'MongoStorageService':{}}
a['fdbStorages'] = fdbNodeStorages
a['fdbNodeRootdir'] = '/home/lisijun/svc_storages/nodes'

path = os.path.split(__file__)[0] + '/' + 'config.json'
json.dump(a,open(path,'w'),indent=4,sort_keys=True)
