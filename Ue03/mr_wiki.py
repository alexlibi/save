# -*- coding: utf-8 -*-
import types
import math
import random

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
    """
    pl=[]
    for i in tl:
        if is_prime_full(i):
            pl.append(i)
    return pl
# ---------------------------------
if __name__=='__main__':
   import sys
   n2t=int(sys.argv[1])
   print n2t,is_prime_full(n2t)
   try:
        a=int(sys.argv[2])
   except:
        sys.exit(0)
   print n2t,mrt_wiki(n2t, a)

