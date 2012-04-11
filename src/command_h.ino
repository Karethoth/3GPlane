#ifndef __COMMAND_H__
#define __COMMAND_H__

// Structure for commands which we receive
struct sCommand
{
  char *command; // The command
  short    argc; // Argument Count
  char   **args; // Arguments
};

void FreeCommand( struct sCommand *cmd );

struct sCommand* LineToCommand( char *line );
int NextSpace( char *line );

#endif

