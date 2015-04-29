import os
from AppService import TxAppService
import config

if __name__ == '__main__':
    appService = TxAppService(config)
    appService.startup()
