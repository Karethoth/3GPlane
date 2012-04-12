import time
import socket
import threading
import SocketServer

HOST = ''
PORT = 1044

plane    = None
client   = None
#observer = None

class ThreadedTCPHandler( SocketServer.BaseRequestHandler ):
  clientType = None
  loggedIn = False

  def handle( self ):
    global plane, client

    self.LogIn()
    self.GetClientType()

    while 1:
      self.data = self.request.recv( 1024 ).strip()

      if( self.data == 'quit' ):
        self.request.close()
        if( self.clientType == 'p' ):
          plane = None
        elif( self.clientType == 'c' ):
          client = None
        break

      if( plane != None and plane != self ):
        plane.request.sendall( self.data + "\n" )
      else:
        print "Not send to plane"
        print plane

      if( client != None and client != self ):
        client.request.sendall( self.data + "\n" )
      else:
        print "Not send to client"
        print client


  def LogIn( self ):
    self.loggedIn = True


  def GetClientType( self ):
    global plane, client
    self.request.sendall( "TYPE: " )
    self.data = self.request.recv( 1024 ).strip()
    if self.data == 'p':
      plane = self
    elif self.data == 'c':
      client = self
    else:
      self.request.sendall( "Wrong type." )
      self.request.close()
      
    self.request.sendall( "You're type is "+self.data + "." )
    self.clientType = self.data


class ThreadedServer( SocketServer.ThreadingMixIn, SocketServer.TCPServer ):
  pass


if __name__ == "__main__":
  server = ThreadedServer( (HOST,PORT), ThreadedTCPHandler )
  ip, port = server.server_address
  server_thread = threading.Thread(target=server.serve_forever)
  server_thread.daemon = True
  server_thread.start()
  print "Server loop running in thread:", server_thread.name
  while 1:
    time.sleep( 1000 )
