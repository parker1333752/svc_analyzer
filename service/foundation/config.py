globalConfig = {
    "cmsStorages": {
        "MongoStorageService": {}, 
        "RawStorageService": {
            "datasetfiles": "/home/lisijun/svc_storages/datasetfiles", 
        }
    }, 
    "fdbStorages": {
        "MongoStorageService": {}, 
        "RawStorageService": {
            #"datasetfiles": "/home/lisijun/svc_storages/dataset", 
            "rawdatafiles": "/home/lisijun/svc_storages/rawdatafiles",
            "rawdatafiles2": "/home/lisijun/svc_storages/rawdatafiles2",
        }
    }, 
    "datasetconfig": {
        "datasetSsid": "dataset",
        "datatableSsid": "datasetfiles",
    },
    "mongohost": "192.168.1.153", 
    "mongoport": 27017
}
