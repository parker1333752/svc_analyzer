import json
import os

def get_config():
    filename = os.path.split(__file__)[0] + '/config.json'
    f = open(filename,'r')
    con = json.load(f)
    f.close()
    return con

def set_config(con=None):
    filename = os.path.split(__file__)[0] + '/config.json'
    if con:
        f = open(filename,'w')
        json.dump(con,f,indent=4,sort_keys=True)
        f.close()
