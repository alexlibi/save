import string,time,signal
import threading
import random

WL=[]
RUN=1

class chief(threading.Thread):
  def __init__(self):
     threading.Thread.__init__(self)
  
  def run(self):
      global WL,RUN
      while RUN:
	tw=random.uniform(1.,10.)
	WL.append(tw)
	w=random.uniform(1.,10.)
        print "Waiting:",w,WL
	time.sleep(w)
#

class worker(threading.Thread):
  def __init__(self):
     threading.Thread.__init__(self)
  def run(self):
      global WL
      try: t=WL.pop()
      except IndexError:
             print "No work" 
             return
      print "%s: Start (%f) %s" % (self.getName(),t,str(WL))
      time.sleep(t)
# -------------------------------------

def breakit(a,b):
    global RUN
    print "Terminated"
    RUN=0
    
    
signal.signal(signal.SIGTERM, breakit)

ch=chief()
ch.start()
for j in range(10):
#  for i in range(5):
       w=worker()
       w.start()
