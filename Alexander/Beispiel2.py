#! /usr/bin/python
#import time
#time.sleep(5)

######################################
#Bibliotheken importieren
######################################

#Um Liste zu splitten
import re
#Um String zu manipulieren
import string
#Fuer sleep
import time


######################################
#Funktionen definieren
######################################

#finde die anzahl der cpus im system
def Get_cpunumber():

    #Datei oeffnen
    fp= open("/proc/stat","r")
    data= fp.readlines()
    fp.close()
    
    #suche in jeder zeile nach "i", da erste zeile nach den cpu-werten mit i beginnt
    for x in xrange(len(data)):
        
        if data[x].find("i",0,1) != -1:
            cpunumber = x
            return cpunumber 
        


#Gesamte CPU Zeit ausgeben (Summe der 10 Einzelwerte pro CPU aus /proc/stat)    
def Read_total_time(data, cpunumber):
    
    #total_time Liste initaialisieren; Liste mit x Eintraegen (x=cpunumber)
    total_time = [0 for x in xrange(cpunumber)]
    
    #total_time wird zeilenweise (CPUweise) aus data berechnet und als liste gespeichert
    for x in xrange(cpunumber):
        for y in xrange(10):
            total_time[x] = total_time[x] + int(data[x][y])
    return total_time

#Liest Datei aus und erstellt eine Liste der Form: [[CPU0],[CPU1], ...] mit [CPU0]= [time0, time1, ..., time9]
#uebergeben wird die Zahl der CPUs
def Read_proc_stat(cpunumber):

    #Datei oeffnen und Zeilenweise in Liste data einlesen, Datei schliessen
    fp= open("/proc/stat","r")
    data= fp.readlines()
    fp.close()

    #Nur die relevanten Elemente behalten (Bei 2 Kernen z.B. die ersten 3 Elemente; gesamt, CPU1, CPU2)
    data= data[:cpunumber] 

    #Einzelenen Integer aus der Liste von Strings herausholen -> data[x][y] ist y-ter Integerwert von x-ter CPU
    for x in xrange(cpunumber):
        #Stript das \n am Ende jeder Zeile
        data[x]= data[x].rstrip("\n")
        #aus dem String wird eine Liste gemacht
        data[x]= data[x].split()
        del data[x][0]
        
    return data

#Ausgabe der Daten. Pro CPU eine Zeile, pro Zeile 10 Eintraege in Prozent mit zwei Nachkommastellen.
def Print_data(data, cpunumber):

    for x in xrange(cpunumber):
        if x== 0:
            print "cpu", "\t|",
        else:
            print "cpu", x-1, "\t|",
        for y in xrange(10):
    
            print '{0:.2f}'.format(data[x][y]), "|", 
        print "\n"
    print "\n"
    return


######################################
#Programmanfang
######################################

#Programmlaufzeit in Sekunden
time_to_run = 100

#Setze Zahl der CPUs+1. (2 CPUs -> 3)
cpunumber = Get_cpunumber()


#data_print initialisieren. (Daten fuer Ausgabe)
data_print = [[0 for i in xrange(10)] for j in xrange(cpunumber)]

#Daten auslesen
data_0 = Read_proc_stat(cpunumber)
#Gesamtzeit auslesen
total_time_0 = Read_total_time(data_0, cpunumber)

for x in xrange(time_to_run):

#sleep fuer eine Sekunde
    time.sleep(1)
    
    #Daten und Gesamtzeit erneut auslesen, damit Differenz gebildet werden kann
    data_1= Read_proc_stat(cpunumber)
    total_time_1 = Read_total_time(data_1, cpunumber)  
    
    #Differenz bilden und durch Zeit dividieren, damit Prozentwert heraus kommt       
    for y in xrange(cpunumber):
        for z in xrange(10):
            data_print[y][z]= int(data_1[y][z])- int(data_0[y][z])
            data_print[y][z]= float(data_print[y][z])/ float((total_time_1[y]-total_time_0[y]))
    
    #Zuerst ausgelesene Daten werden mit Folgedaten ueberschrieben, damit neue Differenz gebildet werden kann.
    data_0, total_time_0= data_1, total_time_1
    
    #Ausgabe mit Fuktion Print_data
    Print_data(data_print, cpunumber)
        
