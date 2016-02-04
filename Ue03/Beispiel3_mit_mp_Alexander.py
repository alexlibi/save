# -*- coding: utf-8 -*-
import types
import math
import random
import time
import sys
import multiprocessing

# ---------------------------------
#(xxx),(y,...) ist die zahl kleiner als xxx muss nur fuer y, ... getestet werden
mr_limits=[(1373653, (2, 3)),
           (9080191, (31, 73)),
           (4759123141, (2, 7, 61)),
           (2152302898747, (2, 3, 5, 7, 11)),
           (3474749660383, (2, 3, 5, 7, 11, 13)),
           (341550071728321, (2, 3, 5, 7, 11, 13, 17)),
           (3825123056546413051, (2, 3, 5, 7, 11, 13, 17, 19, 23)),
           (318665857834031151167461, (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37))
          ]

# ---------------------------------
def mrt_wiki(n, a, dbg=False):  # n ungerade, 1 < a < min(n-1, 2 * (ln n)**2)
    """ Miller Rabin Test ported from
        https://de.wikipedia.org/wiki/Miller-Rabin-Test
        n: number to test
        a: whitness either a number or list
           if a number whitness list is [2,3, ... number]
        return True/False
    """
    if n % 2 == 0: return False

    found=False
    for i in mr_limits:
        if n<i[0]:
           found=True
           break
    if found:
        test_list=i[1]
    elif type(a)== types.IntType:
        test_list=[2]+range(3,a,2)
    elif type(a)== types.ListType:
        test_list=a
    else:
        raise ValueError("Illegal type of a")

    if dbg: print test_list
    n1 = n - 1
    d = n1 >> 1
    j = 1
    while (d & 1) == 0:
        d >>= 1
        j+=1
    for i in test_list:
        t = i
        p = i
        if dbg: print "i=",i
        while d:
           if dbg: print "d=",d," p=",p
           d >>= 1 
           p = p*p % n
           if d & 1:
               t = t*p % n

        if t == 1 or t == n1:
            return True # n ist wahrscheinlich prim
        for k in range(1,j+1):
            t = t*t % n
            if t == n1:
                return True
            if t <= 1:
                break

        return False # n ist nicht prim
    return False
# ---------------------------------
def is_prime_full(n2t):
    """ Test for prime using the full whitness list
        nmax=min(n2t-1,int(2*math.log(n2t)**2))
        return True/False
    """
    nmax=min(n2t-1,int(2*math.log(n2t)**2))
    a=[2]+range(3,nmax,2)
    return mrt_wiki(n2t,a) 
# ---------------------------------
def find_primes(tl):
    """ Find primes from the list tl
        return a new list with primes
        wird aber in diesem Programm nicht verwendet
    """
    pl=[]
    for i in tl:
        if is_prime_full(i):
            pl.append(i)
    return pl
    
    
    
# -------------------------------------
class worker(multiprocessing.Process): #Arbeitet wie Threading.thread nur mit Subprozess
    
    #constructor
    def __init__(self,sta,sto):
        multiprocessing.Process.__init__(self)
        self.sta = sta
        self.sto = sto
    
    #run beschreibt, was gemacht wird
    def run(self):
        primes.extend(prime_list(self.sta, self.sto))
        
      
# -------------------------------------    
#Gibt die Liste mit allen Kanidaten fuer Primzahlen im geschlossenen Intervall (start,ende)
def prime_list(start, end):
    #das wird die liste mit dem primes
    primes = []
    #das ist die zahl die getestet wird
    n2t = start
    
    #for-schleife geht nicht, da xrange keine long als argument akzeptiert und der test auch für sehr grosse zahlen ist
    #daher while-schleife. end+2 damit die zahl end auch getestet wird 
    while n2t < end + 2:
        #wenn die zahl eine primzahl ist kommt sie in die liste
        if is_prime_full(n2t):
            primes.append(n2t)
        #zaehler erhoehen
        n2t = n2t + 1
    return primes
    
# ---------------------------------

manager = multiprocessing.Manager()
primes = manager.list()

if __name__=='__main__':

    st = time.time() #start time
    start = 10**45
    stop = 10**45 + 10**5
    
    #Zahl der Prozessse gleich Zahl der Prozessoren
    n_th = multiprocessing.cpu_count()
    print "Prozesse:", n_th    
    #Liste wird in n_th gleiche Teile geteilt und der erste teil beginnt bei start und endet bei start+offset
    offset = int((stop-start)/n_th)
    
    for x in xrange(n_th):
        if x == n_th-1:
            w = worker(start + offset * x, start + offset * (x+1) - 1 + (stop - start) % n_th)
            #print start + offset * x, start + offset * (x+1) - 1 + (stop - start) % n_th
        else:
            w = worker(start + offset * x, start + offset * (x+1) - 1)
            #print start + offset * x, start + offset * (x+1) - 1
        w.start()
        
    while len(multiprocessing.active_children()) != 1:
        time.sleep(0.1)

    rt = time.time()-st #runtime = time -start time

    print "Gefundene Primzahlen:", len(primes), "| Laufzeit:", rt, "s"#, primes

