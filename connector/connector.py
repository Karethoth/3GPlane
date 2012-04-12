import time
import socket
import threading
import SocketServer

HOST = ''
PORT = 1045

plane    = None
client   = None
#observer = None

class ThreadedTCPHandler( SocketServer.BaseRequestHandler ):
  clientType = None
  loggedIn = False

  def Abort( self ):
    global plane, client

    if( self.clientType == 'p' ):
      plane = None
      print( "Plane disconnected from "+self.client_address[0] )

    elif( self.clientType == 'c' ):
      client = None
      print( "Client disconnected from "+self.client_address[0] )

    self.request.close()


  def handle( self ):
    global plane, client

    self.LogIn()
    self.GetClientType()

    while 1:
      try:
        self.data = self.request.recv( 1024 ).strip()
      except socket.error, msg:
        self.Abort()
        break

      if( len( self.data ) <= 0 ):
        self.Abort()
        break

      if( self.data == 'quit' ):
        self.Abort()
        break

      try:
        if( plane != None and plane != self ):
            plane.request.sendall( self.data + "\n" )
      except socket.error, msg:
        plane.Abort()

      try:
        if( client != None and client != self ):
          client.request.sendall( self.data + "\n" )
      except socket.error, msg:
        client.Abort()
        


  def LogIn( self ):
    self.loggedIn = True


  def GetClientType( self ):
    global plane, client
    self.request.sendall( "TYPE: " )
    self.data = self.request.recv( 1024 ).strip()
    if self.data == 'p':
      plane = self
      print( "Plane connected from " + self.client_address[0] )
    elif self.data == 'c':
      client = self
      print( "Client connected from " + self.client_address[0] )
    else:
      self.request.sendall( "text - Wrong type." )
      self.request.close()
      
    self.request.sendall( "text - Your type is "+self.data + "." )
    self.clientType = self.data


class ThreadedServer( SocketServer.ThreadingMixIn, SocketServer.TCPServer ):
  pass


if __name__ == "__main__":
  server = ThreadedServer( (HOST,PORT), ThreadedTCPHandler )
  ip, port = server.server_address

  server_thread = threading.Thread( target=server.serve_forever )

  server_thread.daemon = True
  server_thread.start()

  while 1:
    time.sleep( 1000 )
