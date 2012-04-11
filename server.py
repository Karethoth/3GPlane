import SocketServer
import serial

throttleMin = 0
throttleMax = 100
throttleMultiplier = (throttleMax-throttleMin)/100.0

HOST = ''
PORT = 1045


arduino = serial.Serial( '/dev/ttyUSB3', 9600 )

class TCPHandler( SocketServer.BaseRequestHandler ):
  def handle( self ):
    while 1:
      self.data = self.request.recv( 1024 ).strip().split( ' ' )
      if self.data[0] == "throttle":
        self.AdjustThrottle( float(self.data[1]) )
      elif self.data[0] == "goodluck":
        self.finish()
        break
      else:
        break

  def AdjustThrottle( self, speed ):
    speed = throttleMin + throttleMultiplier * speed
    cmd = "throttle "+ str(round(speed)) + "!"
    print cmd
    if( not arduino.isOpen() ):
      print( "SERIAL CONNECTION LOST!" )
    else:
      arduino.write( cmd )
      arduino.flush()

if __name__ == "__main__":
  server = SocketServer.TCPServer( (HOST,PORT), TCPHandler )
  server.serve_forever()
