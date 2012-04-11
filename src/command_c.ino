#include "command_h.ino"

// Converts a string to a sCommand struct
struct sCommand* LineToCommand( char *line )
{
  struct sCommand *cmd = (struct sCommand*)malloc(sizeof(struct sCommand));
  int space = NextSpace( line );
  if( space == -1 )
  {
    cmd->command = line;
    cmd->argc    = 0;
  }
  else
  {
    line[space] = '\0';
    cmd->command = line;

    int offset = space;
    space = NextSpace( line+offset+1 );

    cmd->args    = (char**)malloc(sizeof(char**)*2);
    cmd->argc    = 1;
    cmd->args[0] = line+offset+1;

    if( space != -1 )
    {
      cmd->argc    = 2;
      line[offset+space+1] = '\0';
      cmd->args[1] = line+offset+space+2;
    }
  }
  return cmd;
}

// Finds next space
// - Returns -1 if no space was found
int NextSpace( char *input )
{
  int index = 0;
  char c;
  while( (c = input[index]) != 0 )
  {
    if( c == ' ' )
      return index;
    ++index;
  }
  return -1;
}


// Frees a sCommand structure
void FreeCommand( struct sCommand *cmd )
{
  cmd->command = 0;
  free( cmd->args );
  free( cmd );
}

