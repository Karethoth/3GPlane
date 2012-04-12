#ifndef __COMMAND_HANDLER_H__
#define __COMMAND_HANDLER_H__

#include <Servo.h>

#include "command_h.ino"


struct sCommandHandlerVars
{
  int          throttle;
  Servo        esc;
  unsigned int iniTime;
};
extern struct sCommandHandlerVars chVars;


void HandleCommand( struct sCommand *cmd );

void SetThrottle( int throttle );

#endif

