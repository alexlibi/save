import time,signal,sys,os

RUN=1
SUM=0
I=0

def ctrlc(a,b):
    global RUN
    print a,b
    if a==signal.SIGINT:   print "Beendet"
    if a==signal.SIGTERM:   print "Abgebrochen"
    RUN=0

def out(a,b):
    global SUM,I
    print "\n%5d -> %d" % (I,SUM)

    
signal.signal(signal.SIGINT,ctrlc)
signal.signal(signal.SIGTERM,ctrlc)
signal.signal(signal.SIGUSR1,out)

print "pid %d" % (os.getpid())
while RUN:
  SUM+=I
  I+=1
  #time.sleep(0.3)
  #print "loop %d" % (os.getpid()),
  #sys.stdout.flush()





