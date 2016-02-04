import subprocess, sys
#m>1
m = 199017
#a in (1,m-1)
a = 24298
#c in (1,m-1)
c = 99
#y in (0,m-1)
y = 1928

#RANDU
if len(sys.argv) == 2:
	if sys.argv[1] == "RANDU":
		m = 2**31
		a = 2**16 + 3
		c = 0
		y = 1

#C
	if sys.argv[1] == "C":
		m = 2**48
		a = 25214903917
		c = 11
		y = 0

file = "lineare_kongruenz.txt"
file2 = "points_c.txt"
f = open(file,"w")
f2 = open(file2,"w")

for x in xrange(9999):
		y=(a*y+c) % m
		if x > 1:
			f2.write("%s" % bin((y))[2:].zfill(48))
		if (x+1) % 3 == 0:
			f.write("%s\n" % y)
		else:
			f.write("%s\t" % y) 

f.close()
f2.close()

proc = subprocess.Popen(['gnuplot','-p'], stdin=subprocess.PIPE)
proc.stdin.write('set xrange[0:%s]\nset yrange[0:%s]\nset zrange[0:%s]\n'%(m,m,m))
proc.stdin.write('splot "%s"\n' % file)
proc.stdin.write('quit\n')	