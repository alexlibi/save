import random, os

f=open("/home/alexander/python/Ue06/points_rd.txt","w")

for i in xrange(2**20):
	r = random.randint(0, 1)
	f.write("%s" % (r))
	#f.write(bin(int(os.urandom(1).encode('hex'),16))[2:].zfill(8))
f.close()
