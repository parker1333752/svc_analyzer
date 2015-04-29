import vertx
from config import app_config

vertx.deploy_verticle('WebSocketServer.py',app_config.get('socket.config'),1)
vertx.deploy_verticle('HttpServer.py',app_config.get('http.config'),1)
vertx.deploy_verticle('HttpClient.py',app_config.get('http.client.config'),1)
