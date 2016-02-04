import string,time
import threading

#
class worker(threading.Thread):
  def __init__(self,task_list,time_list):
     threading.Thread.__init__(self)
     if task_list:
         self.time=task_list.pop()
         time_list.append(time.time())
     else:
         self.time=-1
# ---------------------------------
  def run(self):
      if self.time<0:
         print "%s: nothing to do" % self.getName()
      print "%s: Start (%f) %f" % (self.getName(),self.time,time.time())
      time.sleep(self.time)
      print "%s: End %s" % (self.getName(),time.ctime())
# -------------------------------------

# Globale Variable
c=10
wl=[x for x in range(10)]
tl=[]
while wl:
  w=worker(wl,tl) # Verwenden immer dieselbe Liste, Referenzen werden uebergeben
  w.start()
  c-=1

print tl
print "%d remaining threads" % (threading.activeCount()-1)
