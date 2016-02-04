#! /usr/bin/python
#Angabe des Interpretors
import string

#! /usr/bin/python


# -*- coding: utf-8 -*-

######################################
#Hello World Programm
######################################

#print "Hello World or so?!"	

######################################
#gibt den Wert von i^2 aus
######################################

##Ist die Eingabe eine ganze Zahl? Falls nicht neuen Input anfordern.
#while True:
#    try:
#        i = int(raw_input("Zu quadrierende Zahl angeben: i = "))
#        break
#    except ValueError:
#        print 'Das war keine ganze Zahl!'

##Rechnung ausfueren und ausgeben      
#i = i ** 2						
#print "Das Quadrat von i ist gleich", i

######################################
#Ausgegebener Wert ist Summe der vorangegangenen
######################################

#a, b = 0, 1						
#while b < 10:
#	print b
#	a, b = b, a+b 


######################################
#Gibt an, ob eine eingegebene Zahl groesser, kleiner oder gleich 0 ist
######################################

#x=int(raw_input('Ganze Zahl eingeben: '))
#if x < 0:
#	x = 0
#	print "Zahl ist kleiner als Null"
#elif x == 0:
#	print  "Zahl ist gleich Null"
#else:
#	print "Zahl ist groesser als 1"

x
######################################
#Bibliotheken importieren
######################################

#import math

#print math.sqrt(2.)

######################################
#Datei oeffnen; Jede Zeile als Listenelement
######################################

#fp= open("a.dat,"r")

#data= fp.readlines()

#fp.close()

######################################
#For Schleife
######################################

#liste= range(10)

#for x in xrange(10):

#    liste[x]= liste[x]*2
#    
#print liste

######################################
#Listen-Manipulation
######################################

#liste= ["a","b","c","d"]

#liste.remove("b")

#print liste

######################################
#String-Manipulation
######################################

#txt= "hallo \n tests"

#txt= string.replace(txt,"\n","")

#print txt

######################################
#Liste mit 0 fuellen
######################################

#x = [0 for i in xrange(5)]

#x = [[0 for i in xrange(5)] for i in xrange(3)]
#print x

######################################
#range/xrange
######################################

#a = range(10)
#b = range(5,10)

#print a, b

######################################
#length
######################################

#a = [1,'12',3]
#b = ['1']
#c = '12'

#print len(a), len(b), len(c)

######################################
#ueberpruefen, ob elemente einer liste listen sind
######################################

a = [1,2,[3,4],5]

for k in xrange(len(a)):
    if isinstance(a[k], list):
        print k
        
