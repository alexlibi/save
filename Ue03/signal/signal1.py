import string,time,signal,sys
import threading
import random

RUN=1

def breakit(a,b):
    global RUN
    print "Signal:",a,b
    RUN=0

signal.signal(signal.SIGTERM, breakit)
signal.siginterrupt(signal.SIGTERM,False) # avoid interrupted system call

while RUN:
      time.sleep(0.2)
      print "x",
      sys.stdout.flush()
