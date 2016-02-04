import sys,time,os

D={}
n_th=8

def teiler(z):
   tl=[]
   t=2
   while(z/t>=1):
	if z%t==0:
	   tl.append(t)
	   t=2
	   z/=t
	else: t+=1
   return tl
# -------------------------------------

s=10000000
zl=range(s,s+10)
n_p=4
ts=time.time()
pl=[]
while 1:
    if zl==[]:break
    z=zl.pop()
    istat=os.fork()  ##Verzweigung
    if istat!=0:
       print "Parent:",istat,zl,D
       sys.stdout.flush()
    if istat==0:
       D[z]=teiler(z)
       print "Child:",os.getpid(),os.getpgrp(),z,zl,D
       sys.stdout.flush()
       sys.exit(0)
print os.getpid(),os.getpgrp()
print os.waitpid(0,0)
dt=time.time()-ts
print "Ergebnis:",D
print "Zeit:",dt

# Arbeitet nicht wie erwartet:
# Die Subprozesse fuellen zwar ihre eignen Ergebnisdicts (D) aus,
# am Ende bleibt jedoch D leer
# Da fuer jeden Subprozess eine Kopie des Ausgangsprozesses (parent)
# im Speicher angefertigt wird.
# Die einzelnen Subprozesse (child) erfahren nichts von der Veraenderung
# der (globalen) Variablen (zl)
#
# Damit die Aenderungen weitergegeben werden:
# IPC
