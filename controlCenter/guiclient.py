import pygame
from pygame import locals

import socket

import pygtk
import gtk


HOST, PORT = 'ndirt.com', 1045

sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )


def AdjustThrottle( speed ):
  speed = speed.value
  cmd = "throttle "+ str(round(speed))+"!"
  #print cmd
  sock.sendall( cmd )

class GUI:
  def destroy( self, widget, data=None ):
    gtk.main_quit()

  def __init__( self ):
    self.window = gtk.Window( gtk.WINDOW_TOPLEVEL )
    self.window.connect( "destroy", self.destroy )
    self.window.set_border_width( 10 )
    self.window.set_title( "GUI" )

    self.container = gtk.VBox( False, 10 )

    self.throttleAdj = gtk.Adjustment( 0, 0, 100, 1, 1, 1 )
    self.throttleAdj.connect( "value_changed", AdjustThrottle )
    self.throttle = gtk.VScale( self.throttleAdj )
    self.throttle.set_inverted( True )

    self.container.add( self.throttle )
    self.window.add( self.container )

    self.throttle.show()
    self.container.show()
    self.window.show()


  def main( self ):
    try:
      sock.connect( (HOST,PORT) )
      sock.setsockopt( socket.IPPROTO_TCP, socket.TCP_NODELAY, 1 )
      sock.sendall( "c" )
      gtk.main()
    finally:
      sock.close()


if __name__ == "__main__":
  cp = GUI()
  cp.main()
