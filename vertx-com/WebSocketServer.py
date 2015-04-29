import vertx
from core.event_bus import EventBus

config = vertx.config()
server = vertx.create_http_server()

@server.websocket_handler
def websocket_handler(socket):

    def getUUID():
        s = socket.toString()
        return s.split('@')[-1]

    uuid = getUUID()
    #print 'uuid =',uuid

    @socket.data_handler
    def data_handler(buff):
        resp_data = '%r'%buff
        message = {'uuid':uuid,'message':resp_data}
        EventBus.publish('send.mycommand',message)
        print 'websocket receive:',resp_data
        # socket.write_text_frame(resp+'\n')

        if socket.write_queue_full:
            socket.pause()
            @socket.drain_handler
            def drain_handler():
                socket.resume()

    @socket.close_handler
    def close_handler():
        #EventBus.unregister_handler('receive.myresult'+uuid,resultHandleId)
        EventBus.unregister_handler(resultHandleId)
        print 'closed websocket',uuid

    def receive_error(msg):
        socket.write_text_frame('error: '+str(msg)+'\n')

    def receive_result(msg):
        socket.write_text_frame(str(msg.body))

    EventBus.register_handler('receive.error',handler=receive_error)
    resultHandleId = EventBus.register_handler('receive.myresult'+uuid,handler=receive_result)
    
    print 'hello websocket',uuid

server.listen(config['port'],config['host'])

