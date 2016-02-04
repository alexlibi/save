import sys,time

def teiler(z):
   """ Berechnet Teiler einer Zahl
       Rueckgabe: Liste mit Teilern
   """
   tl=[]
   t=2
   while(z/t>=1):
	if z%t==0:
	   tl.append(t)
	   #t=2
	   #print z,t
	   z/=t
	else: t+=1
   return tl
	
if __name__=='__main__':
  #print teiler.__doc__
#  print teiler(int(sys.argv[1]))
#  sys.exit(0)
  d={}
  ts=time.time()
  s=10000000
  for i in range(s,s+int(sys.argv[1])):
      d[i]=teiler(i)
  dt=time.time()-ts
  print d
  print dt
