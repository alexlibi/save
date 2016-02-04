import sys, socket, math, numpy as np
from collections import Counter
host = ''
port = 56700

#returns list of lists
def list_of_string_to_list_list(liste,dice,throws):
	number_set=[[0 for i in xrange(throws)]for j in xrange(dice)]
	for i in xrange(dice):
		for j in xrange(throws):
			number_set[i][j]=int(liste[i][j])
	return number_set

def mean(liste):
	return np. mean(liste)
	#return float(sum(liste))/len(liste)


def entropy(s):
	#p, lns = Counter(s), float(len(s))
	#return -sum( count/lns * math.log(count/lns, 2) for count in p.values())
	return np.entropy(liste)
	
def var(liste):
	#m=mean(liste)
	#var=0
	
	#for i in xrange(len(liste)):
	#	var+=(liste[i]-m)**2
	#var = float(var)/len(liste)
	#return var
	return np.var(liste)
#returns string
def request(throws, dice):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect((host, port))
		
	except socket.error as msg:
		s.close()
		s = None
		
	if s == None:
		print 'keine verbindung'
		sys.exit(1)
	else:
		s.sendall("throw %s %s" %(throws,dice) + "\n")
		data=""
		while 1:
			buf = s.recv(1024)
			if not len(buf):
				s.close()
				return data.strip()
				break
			data+=buf


liste = [] 
dice=20
throws=10000

for i in xrange(dice):
	liste.append(request(throws, i))

liste=list_of_string_to_list_list(liste,dice,throws)

for i in xrange(dice):
	print i+1, "Mittelwert:", mean(liste[i]),"Standardabweichung:", var(liste[i])**0.5, "Entropie:", entropy(liste[i])
