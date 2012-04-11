import pygtk
pygtk.require('2.0')
import gtk

import threading
import gobject
import time

gobject.threads_init()

import serial
import pygame
from pygame import locals

arduino = serial.Serial( '/dev/ttyUSB0', 9600 )

pygame.init()
pygame.joystick.init()

joystickEnabled = False

try:
  j = pygame.joystick.Joystick( 0 )
  j.init()
  print( 'Enabled joystick: ' + j.get_name() )
  joystickEnabled = True
except pygame.error:
  print( 'no joystick found' )



class ControlPanel:
  def destroy( self, widget, data=None ):
    gtk.main_quit()

  def __init__( self ):
    self.window = gtk.Window( gtk.WINDOW_TOPLEVEL )
    self.window.set_border_width( 10 )
    self.window.set_title( "Control Panel" )
    self.window.resize( 230, 300 )

    self.throttle_label = gtk.Label( "Throttle" )

    throttle_adj = gtk.Adjustment( 00.0, 00.0, 100.0, 1.0, 10.0, 0.0 )
    throttle_adj.connect( "value_changed", self.AdjustThrottle )
    self.throttle = gtk.VScale( throttle_adj )
    self.throttle.set_inverted( True )
    self.throttle.set_update_policy( gtk.UPDATE_CONTINUOUS )

    
    self.window.connect( "destroy", self.destroy )
    gobject.idle_add( IdleFunc, self )

    self.box1 = gtk.VBox( False, 0 )
    self.window.add( self.box1 )
    self.box1.pack_start( self.throttle_label, False, False, 0 )
    self.box1.pack_start( self.throttle, True, True, 0 )
    self.throttle_label.show()
    self.throttle.show()
    self.box1.show()
    self.window.show()

  def main( self ):
    gtk.main()
    arduino.close()

  def AdjustThrottle( self, speed ):
    speed = 20 + (49.0/100.0) * (speed.value)
    cmd = "throttle "+ str(round(speed)) + "!"
    print cmd
    if( not arduino.isOpen() ):
      print( "SERIAL CONNECTION LOST!" )
    else:
      arduino.write( cmd )
      arduino.flush()

if __name__ == "__main__":
  cp = ControlPanel()
  cp.main()
