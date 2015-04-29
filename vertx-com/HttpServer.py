import vertx
from core.event_bus import EventBus

config = vertx.config()
server = vertx.create_http_server()

@server.request_handler
def request_handler(req):

    @req.body_handler
    def body_handler(buff):
        if req.path == '/myresult':
            uuid = req.params.get('uuid')
            #print 'uuid=%s'%uuid
            EventBus.send('receive.myresult'+uuid,buff)
            print 'http server result:',buff


    if req.path == '/myresult':
        req.response.end('vertx ok')

    else:
        req.response.end('unknown request')


server.listen(config['port'],config['host'])
