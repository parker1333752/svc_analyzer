import vertx
from core.event_bus import EventBus

config = vertx.config()
client = vertx.create_http_client()
client.port = config['remote_port']
client.host = config['remote_host']

def command_response(resp):
    '''response of send command to analyzer
    '''
    @resp.body_handler
    def receive(buff):
        if resp.status_code != 200:
            EventBus.send('receive.error',resp.status_code)

        #print 'rt_code =',resp.status_code
        # print 'buff=<%r>'%str(buff)

def command_request(msg):
    '''send command to analyzer
    '''
    send_data = msg.body.get('message')
    args = '?uuid=%s'%msg.body.get('uuid')
    msg.reply('')

    request = client.post('/myconsole'+args, command_response)
    #request.put_header('Content-Type','application/json')
    request.put_header('Content-Length',str(len(send_data)))
    request.write_str(send_data)
    request.end()

EventBus.register_handler('send.mycommand',handler=command_request)

