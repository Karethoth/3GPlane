#include "command_handler_h.ino"

struct sCommandHandlerVars chVars;


void SetThrottle( int throttle ){
  int angle = map( throttle, 0, 100, 0, 180 );
  chVars.throttle = throttle;
  chVars.esc.write( angle );
}


void HandleCommand( struct sCommand *cmd )
{
  // THROTTLE
  if( strcmp( cmd->command, "throttle" ) == 0 &&
      cmd->argc >= 1 )
  {
    chVars.throttle = atoi( cmd->args[0] );
    SetThrottle( chVars.throttle );
  }

  // GETTHROTTLE
  else if( strcmp( cmd->command, "getThrottle" ) == 0 )
  {
    Serial.print( "Throttle: " );
    Serial.println( chVars.throttle );
  }
}
