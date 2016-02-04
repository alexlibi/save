/**********************************************************************/
/* shell5.c                                                           */
/*                                                                    */
/* Wie shell4, aber unter Verwendung von execvp statt system          */
/*                                                                    */
/* Parent terminiert altes xterm mit kill() nach der Eingabe eines    */
/* neuen commands.                                                    */
/*                                                                    */
/*                                                                    */
/**********************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <error.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <signal.h>
#include <string.h>

int main()
{int istat=0;
 char befehl[256];
 char prompt[]="MyPrompt=> ";
 int fd0, fd1, fd2;
 while(1)                         // Endlosschleife des parent-Prozesses 
 {printf("\n%s",prompt);
  fgets(befehl,256,stdin);
  if(istat) kill(istat, SIGTERM); // terminiere alten child-Prozess
  if(!strlen(befehl)) continue;    // ignoriere leeren input
  if(!strncmp(befehl,"exit",4) ) exit(0);
  istat=fork();                   //Verzweigung
// child
  if(istat==0)                    //Child-Prozess fuehrt den Befehl aus 
  {char befehl_neu[512]="xterm -fn 10x20 -hold -e ";
   int i, argc=0;
   char* argv[20];
   strcat(befehl_neu,befehl);
   argv[0]=befehl_neu;            // aufzurufendes Programm = 1. Parameter
   for(i=1;i<255;++i) 
   {if(befehl_neu[i]=='\0') break;                 // fgets schliesst mit \0 ab
    if(befehl_neu[i]<=' ') befehl_neu[i]='\0';      // Substring abschliessen
    if(befehl_neu[i]>' ' && befehl_neu[i-1]=='\0')  //neuer Einzelparameter
    {argv[++argc]=&befehl_neu[i];
    }
   }
   argv[++argc]=NULL;
   execvp(argv[0], argv); exit(0); //ausfuehren und terminieren
  }
// Ende child
}}   
