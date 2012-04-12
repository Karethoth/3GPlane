#include <Servo.h>
#
#include "command_h.ino"
#include "command_handler_h.ino"


/** DEFAULT VALUES **/
#define DEFAULT_THROTTLE 20
#define INI_TIME         5000

/** PINS **/
#define PIN_ESC          9



// Define pins
int escPin = PIN_ESC;



// Variables for the loop
char strBuffer[101];
int  inByte;
int  strLength = 0;


// Function to arm the esc
void ArmEsc(){
  SetThrottle( chVars.throttle );
  delay( chVars.iniTime );
}


void HandleInput()
{
  if( Serial.available() > 0 )
  {
    inByte = Serial.read();
    if( inByte == '\n' ||
        inByte == '\0' ||
        inByte == '!' )
    {
      int length = strLength;
      strBuffer[strLength+1] = 0;

      struct sCommand *cmd = LineToCommand( strBuffer );

      HandleCommand( cmd );
      FreeCommand( cmd );

      memset( strBuffer, 0, strLength );
      strLength = 0;
    }
    else
    {
      strBuffer[strLength++] = inByte;
    }
  }
}


void setup()
{
  // Basic settings
  chVars.throttle = DEFAULT_THROTTLE;
  chVars.iniTime  = INI_TIME;

  // Set up the serial connection
  Serial.begin( 9600 );

  // Attach the esc
  chVars.esc.attach( escPin );

  // Arm the esc
  ArmEsc();
}


void loop()
{
  HandleInput();
}

