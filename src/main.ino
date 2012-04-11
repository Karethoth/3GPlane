#include <Servo.h>
#include "command_h.ino"

char buffer[101];
int inByte;
int n;

int escPin = 9;
int throttle = 20;
Servo esc;


void setup()
{
  Serial.begin( 9600 );
  n = 0;
  esc.attach( escPin );
  arm();
}

void loop()
{
  if( Serial.available() > 0 )
  {
    inByte = Serial.read();
    if( inByte == '\n' ||
        inByte == '\0' ||
        inByte == '!' )
    {
      int length = n;
      buffer[n+1] = 0;
      n = 0;
      /*Serial.println();*/
      /*Serial.print( "Received: " );*/
      /*Serial.println( buffer );*/
      struct sCommand *cmd = LineToCommand( buffer );
      /*Serial.print( "command was: " );*/
      /*Serial.println( cmd->command );*/
      /*if( cmd->argc > 0 )*/
      /*{*/
      /*  Serial.print( "Arg1: " );*/
      /*  Serial.println( cmd->args[0] );*/
      /*  if( cmd->argc > 1 )*/
      /*  {*/
      /*    Serial.print( "Arg2: " );*/
      /*    Serial.println( cmd->args[1] );*/
      /*  }*/
      /*}*/
      HandleCommand( cmd );
      FreeCommand( cmd );
      memset( buffer, 0, length );
      /*Serial.println();*/
    }
    else
    {
      buffer[n++] = inByte;
    }
  }
  //setSpeed( throttle );
}


void arm(){
  // arm the speed controller, modify as necessary for your ESC  
  setSpeed( 20 );
  delay( 10000 ); //delay 10 second,  some speed controllers may need longer
}


void setSpeed( int speed ){
  // speed is from 0 to 100 where 0 is off and 100 is maximum speed
  //the following maps speed values of 0-100 to angles from 0-180,
  // some speed controllers may need different values, see the ESC instructions
  int angle = map( speed, 0, 100, 0, 180 );
  esc.write( angle );    
}




void HandleCommand( struct sCommand *cmd )
{
  // THROTTLE
  if( strcmp( cmd->command, "throttle" ) == 0 &&
      cmd->argc >= 1 )
  {
    throttle = atoi( cmd->args[0] );
    setSpeed( throttle );
  }

  // GETTHROTTLE
  else if( strcmp( cmd->command, "getThrottle" ) == 0 )
  {
    Serial.print( "Throttle: " );
    Serial.println( throttle );
  }
}
