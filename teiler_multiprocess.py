import sys,time,os
import multiprocessing
import random

def teiler(z):
   tl=[]
   t=2
   while(z/t>=1):
	if z%t==0:
	   tl.append(t)
	   z/=t
	else: t+=1
   return tl
# -------------------------------------
class worker(multiprocessing.Process): #Arbeitet wie Threading.thread nur mit Subprozess
  def __init__(self,z):
     multiprocessing.Process.__init__(self)
     self.z=z

  def run(self):
      D[self.z]=teiler(self.z)
      #time.sleep(0.1)
# -------------------------------------

n_th=2
#s=100000000
s=10000000
manager = multiprocessing.Manager() #Ermoeglicht Datenaustausch zw. Prozessen

#Globale Variablen
D = manager.dict() # Erstellt ein Dict auf das alle Subprozesse zugreifen koennen (shared memory)
zl = manager.list(range(s,s+200)) # Erstellt ebenso eine Liste

dcnt=0
print zl
th_l=[]
ts=time.time()
run=2
while run:
 if not zl:break
 #print multiprocessing.active_children()
 if len(multiprocessing.active_children())-1<n_th:
   #MUTEX.acquire()
   z=zl.pop()
   #MUTEX.release()
   w=worker(z)
   th_l.append(w)
   w.start()
   #print "processes:",len(multiprocessing.active_children())-1
 #run-=1
for t in th_l: t.join()
dt=time.time()-ts
print zl
print D
print dt,"seconds active"

