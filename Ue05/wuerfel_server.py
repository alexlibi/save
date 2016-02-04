# -*- coding: utf-8 -*-
import string, sys, os, time
import SocketServer
from random import *

# -------------------------------------

def dice(n,z,sep=""):
    """Liefert n zufällige Ziffern
       Aufruf: wurf.py -n # Auswahlliste

       n #: Anzahl der Würfe
       z string:  Auswahlliste:
                 23: Ohne Trennzeichen: Hängt die Kombination an die Auswahlliste
        1,2,3,4,5,6:  Mit trennzeichen: Hängt jedes einzelne onjekt an die Auswahlliste
                ' ': Kombiniert die beiden oberen

        z.B: 12345: Hängt [12345] an die Auswahlliste -> 1 2 3 4 5 1 2 3 4 5 ...
           12 1,2,3,4,5: -> Gleichverteilt: 1,2 als Folge und 1 2 3 4 5
           10*1 10*2 10*3 10*4 10*5 11*6: 10 1er, 10 2er, ... 11 6er 
           1,2,3,4,5,6: Fairer Würfel
           1,2,2,3,3,4,4,5,5,6: Prisma, Achse 1-6
           1,1,2,3,4,5,6,6: Flaches Prisma (1-6)
           1,2,3,4,5,6,6,6: 6 Schwerer
           2,3,4,5,6,6: 1er mit 6 übermalt
        sep: Trennzeichen
    """

    wl=[]
    for o in z.split():
      l=o.split(',')
      #print "l",l
      if len(l)==1:
         if l[0].find("*")!=-1:
            ll=l[0].split("*")
            mult=int(ll[0])
            for i in range(mult): wl.append(ll[1])
         else:wl.append([i for i in l[0]])
      else:
        for i in l: wl.append(i)
  
    i=0
    ret=""
    print wl
    while i<n:
        r=choice(wl)
        try: a=r[0]
        except: 
           ret+=r+sep
           i+=1
        else:
           ret+=string.join(a,sep)
           i+=len(a)
    return ret
# Handles request simultaneously
#
# ---------------------------------------------
# ---- Socket Handler
# ---------------------------------------------
syntax="""Syntax: throw p1 p2
                  p1: number of dices
                  p2: number (type of dice)
       """
p2_dict={0:"1,2,3,4,5,6",
         1:"1,2,3,3,4,4,5,5,6,6,12",
         2:"1,1,2,3,4,4,5,5,6,6,23",
         3:"1,1,2,2,3,4,5,5,6,6,34",
         4:"1,1,2,2,3,3,4,5,6,6,34",
         5:"1,1,2,2,3,3,4,5,6,6,45",
         6:"1,1,2,2,3,3,4,4,5,6,56",
         7:"1,1,2,3,4,5,6",
         8:"3*1 2*2 2*3 2*4 2*5 2*6",
         9:"4*1 3*2 3*3 3*4 3*5 3*6",
         10:"5*1 4*2 4*3 4*4 4*5 4*6",
         11:"1,2,2,3,4,5,6",
         12:"2*1 3*2 2*3 2*4 2*5 2*6",
         13:"3*1 4*2 3*3 3*4 3*5 3*6",
         14:"4*1 5*2 4*3 4*4 4*5 4*6",
         15:"1,2,2,3,3,4,3,5,5,6",
         16:"1,1,2,3,3,4,4,5,6,6",
         17:"1,1,2,3,4,5,6,6",
         18:"1,2,3,4,5,6,6,6",
		 19:"2,3,4,5,6,6",
        }
class CommandHandler(SocketServer.StreamRequestHandler):
  def handle(self):
     try: line=self.rfile.readline().lower().strip().split()
     except:
        self.wfile.write("Bad command\n")
        return
     if not line:
        self.wfile.write("Bad command\n")
        return
  
     if line[0]=="help":
        self.wfile.write(syntax+"\np2:")
        self.wfile.write(str(p2_dict.keys())+'\n')
        return
     elif line[0]=="throw":
        try:
          p1=int(line[1])
          p2=int(line[2])
        except:
          self.wfile.write("Bad or missing parameter p1 or p2\n")
          return
        try:z=p2_dict[p2]
        except:
          self.wfile.write("Parameter p2 out of range %s\n" % str(p2_dict.keys()))
          return
        r=dice(int(p1),z)+'\n'
        self.wfile.write(r)
        print "daten gesendet"
     else:
        self.wfile.write("Illegal command: %s\n" % line)
     return
# ---------------------------------------------



#Start socket server
server = SocketServer.ThreadingTCPServer(('',56700),CommandHandler)

while 1:
   server.handle_request()
   


