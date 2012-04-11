import pygame
from pygame import locals

import socket


HOST, PORT = 'home.ndirt.com', 1044

sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

pygame.init()
pygame.joystick.init()

joystickEnabled = False

def AdjustThrottle( speed ):
  speed = speed * -50+50
  cmd = "throttle "+ str(round(speed))+" "
  #print cmd
  sock.sendall( cmd )


try:
  j = pygame.joystick.Joystick( 0 )
  j.init()
  print( 'Enabled joystick: ' + j.get_name() )
  joystickEnabled = True
except pygame.error:
  print( 'no joystick found' )

try:
  sock.connect( (HOST,PORT) )
  while 1:
    for e in pygame.event.get():
      if e.type == pygame.locals.JOYAXISMOTION:
        z = j.get_axis(2)
        AdjustThrottle( z )
        
finally:
  sock.close()


if __name__ == "__main__":
  cp = ControlPanel()
  cp.main()
