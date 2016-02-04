import sys,time,os
import threading,thread
import random

D={}
MUTEX=thread.allocate_lock()

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
class worker(threading.Thread):
  def __init__(self,z):
     threading.Thread.__init__(self)
     self.z=z

  def run(self):
      D[self.z]=teiler(self.z)
      #time.sleep(0.1)
# -------------------------------------

n_th=16
s=10000000
zl=range(s,s+200)
#dcnt=0
ts=time.time()
while 1:
 if zl==[]:break
 if threading.activeCount()-1<n_th:
  MUTEX.acquire()
  z=zl.pop()
  MUTEX.release()
  w=worker(z)
  w.start()
print "End:",threading.activeCount()-1," threads are still active"
#while threading.activeCount()>1: time.sleep(0.1)
w.join()
dt=time.time()-ts
print D
#print dcnt,dt
print dt,"seconds active"

