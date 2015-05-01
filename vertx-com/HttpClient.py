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
        pass

def command_request(msg):
    '''send command to analyzer
    '''

    msg.reply('')
    send_data = msg.body.get('message')
    args = '?uuid=%s'%msg.body.get('uuid')

    request = client.post('/myconsole'+args, command_response)
    request.put_header('Content-Length',str(len(send_data)))
    request.write_str(send_data)
    request.end()

EventBus.register_handler('send.mycommand',handler=command_request)

