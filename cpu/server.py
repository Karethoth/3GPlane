import socket
import serial

throttleMin = 0
throttleMax = 100
throttleMultiplier = (throttleMax-throttleMin)/100.0

HOST = 'localhost'
PORT = 1045


arduino = serial.Serial( '/dev/ttyUSB0', 9600 )


sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )


def Handle():
  global sock
  while 1:
    try:
      data = sock.recv( 1024 ).strip()
      if( len( data ) <= 0 ):
        break
      data = data.split( ' ' )
    except socket.error, msg:
      break
    print data
    if data[0] == "throttle":
      AdjustThrottle( float(data[1]) )
    elif data[0] == "TYPE:":
      sock.sendall( "p" )
    elif data[0] == "goodluck":
      break
    else:
      continue


def AdjustThrottle( speed ):
  speed = throttleMin + throttleMultiplier * speed
  cmd = "throttle "+ str(round(speed)) + "!"
  print cmd
  if( not arduino.isOpen() ):
    print( "SERIAL CONNECTION LOST!" )
  else:
    arduino.write( cmd )
    arduino.flush()


try:
  sock.connect( (HOST,PORT) )
  Handle()
finally:
  sock.close()

