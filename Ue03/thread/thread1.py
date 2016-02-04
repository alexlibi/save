import string,time,os
import threading

class worker(threading.Thread):
  # Document string; auf Einrueckung achten
  """ Generiert threads, die eine bestimmte Zeit warten
  """
  def __init__(self,time):
     """ time: Wartezeit
     """
     threading.Thread.__init__(self)
     self.time=time
     
  def run(self):
      """ Wird mit der methode Thread.start() aufgerufen
      """
      print "%s: Start %s (%d s, pid: %d)" % (self.getName(),time.ctime(),self.time,os.getpid())
      time.sleep(self.time)
      print "%s: End %s" % (self.getName(),time.ctime())
# -------------------------------------
print "main pid: %d" % os.getpid()
while 1: 
  s=raw_input("Zeit [s]: ")
  try: t=int(s)
  except:
      print "Eine Zahl bitte!!"
      continue
  if t<0: break
  if t>200:
      print "Eine Zahl 0 ... 200"
      continue
      
  w=worker(t) # generiert einen neuen thread (worker)
  w.start()   # Startet den thread
  
print "%d remaining threads" % (int(threading.activeCount())-1)




