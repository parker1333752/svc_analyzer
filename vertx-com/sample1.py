# 
# Sample of TCP server 
# 
# required:
# -- vert.x
# -- JVM
# 
# step by step:
# 1. in command line window (win+r and enter 'cmd'), switch to the fold contain this file, 
#       and enter 'vertx run sample1.py'
# 2. in command line window , enter 'telnet localhost 1234'.
# 3. see what happen when you tab the keyboard.

import vertx

server = vertx.create_net_server()

@server.connect_handler
def connect_handler(socket):
    vertx.logger().info('I am connected')

    @socket.data_handler
    def receive(buffer):
        vertx.logger().info('receive %d bytes of data, <%s>'%(buffer.length,buffer))

    def period_send(tid):
        socket.write_str('hello socket\r\n')
    tid=vertx.set_periodic(1000,period_send)

    @socket.close_handler
    def closed():
        vertx.logger().info('I am disconnected')

def listen_handler(err, server):
    if err is None:
        vertx.logger().info('Server is listen OK')
    else:
        err.printStackTrace()

def vertx_stop():
    print 'doing something cleanup.'

server.listen(8000,'0.0.0.0',listen_handler)
