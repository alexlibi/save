import sys,time,os
import multiprocessing


def teiler(z):
   tl=[]
   t=2
   rz=z
   while(z/t>=1):
	if z%t==0:
	   tl.append(t)
	   z/=t
	else: t+=1
   return dict({rz:tl})
# -------------------------------------
if __name__ == '__main__':
    #s=100000000
    s=10000000

    ts=time.time()
    pool = multiprocessing.Pool(processes=16)    # start 8 worker processes
    r=pool.map(teiler, range(s,s+200))    # prints "[0, 1, 4,..., 81]"
    dt=time.time()-ts
    print r
    print dt,"seconds active"

