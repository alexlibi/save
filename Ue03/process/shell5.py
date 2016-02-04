##/**********************************************************************/
##/* shell5.py                                                           */
##/*                                                                    */
##/* Wie shell4, aber unter Verwendung von execvp statt system          */
##/*                                                                    */
##/* Parent terminiert altes xterm mit kill() nach der Eingabe eines    */
##/* neuen commands.                                                    */
##/*                                                                    */
##/*                                                                    */
##/**********************************************************************/

import sys,os,signal
prompt="MyPrompt=> "
istat=0

while 1:                          ## Endlosschleife des parent-Prozesses 
  befehl=raw_input(prompt)
  print "Parent:",os.getpid(),"istat:",istat
  if istat:
     print "Terminating",istat
     os.kill(istat, signal.SIGTERM)  ## terminiere alten child-Prozess
     print "Terminating",istat
  if not befehl:
 continue        ## ignoriere leeren input
  if befehl=="exit": sys.exit(0)
  istat=os.fork()                   ##Verzweigung
## child
  if istat==0: ##Child-Prozess fuehrt den Befehl aus 
     print "Child: ",os.getpid()," Parent:",os.getppid(),"Befehl:", befehl
     befehl_neu="/usr/bin/xterm"
     args="-fn10x20 -hold -e".split()               
     args=args+befehl.split()
   
     os.execvp(befehl_neu, args)
     sys.exit(0) ##ausfuehren und terminieren
## Ende child
