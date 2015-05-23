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
            "rawdatafiles": "/home/lisijun/svc_storages/rawdatafiles"
            #"rawdatafiles": "/home/lisijun/svc_storages/rawdata"
        }
    }, 
    "mongohost": "192.168.1.153", 
    "mongoport": 27017
}
