import random, math, os, subprocess

file = "points.txt"	
N = []

#set up N
for i in xrange(3,20):
	N.append(2**i)

#calculate pi with mc
def calc_pi(N):
	k = 0
	#file = "/home/alexander/python/Ue06/points.txt"
	#f = open(file, "w")
	for n in xrange(N):
		#x, y = random.random(), random.random()
		x, y = float(int(os.urandom(4).encode('hex'),16)) / 4294967295, float(int(os.urandom(4).encode('hex'),16)) / 4294967295
		#f.write("%s\t%s\n" % (x, y))
		if (x**2 + y**2) < 1:
			k += 1
	if k!=0: 
		pi = k / float(n) * 4
		return pi
	#f.close()

def plot_delta(file):
	proc = subprocess.Popen(['gnuplot','-p'], stdin=subprocess.PIPE)
	proc.stdin.write('xrange=(0,6)\n')
	proc.stdin.write('plot "%s" pt 7, 0\n' % file)
	proc.stdin.write('quit\n')	
	
#open file used for plot
f = open(file,"w")	

#calc pi for N points with the different N
for i in N:
	my_pi = calc_pi(i)
	if my_pi != None:
		delta  = my_pi - math.pi
		f.write("%s\t%s\n" % (math.log(i,10), delta))
		print "N =", i, "\t", my_pi, "\t", delta

f.close()

plot_delta(file)