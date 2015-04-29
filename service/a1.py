from HttpClient import TxHttpClient
from config import consoleConfig as globalConfig
import time

a = TxHttpClient()
a.connect(globalConfig['remote_host'],globalConfig['remote_port'])

while True:
    a.post(globalConfig['remote_path'],'test hello')
    time.sleep(1)
