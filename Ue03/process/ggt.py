def ggt(x,y):
   z=max(x,y)
   n=min(x,y)
   count=1
   while n :
     q=z%n
     z=n
     n=q
     count+=1
   return z,count 
def kgv(x,y):
   return x*y/ggt(x,y)[0]

if __name__=='__main__':

    from random import *
    import sys

    start=10**1500+1
    end=10**1501
    n1=randrange(start,end,2)   
    n2=randrange(start,end,2)  

    print n1,n2,ggt(n1,n2)
    print kgv(n1,n2)
    n1=int(sys.argv[1])
    n2=int(sys.argv[2])
    print n1,n2,ggt(n1,n2)
    print kgv(n1,n2)

