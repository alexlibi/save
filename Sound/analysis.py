import math
import numpy
import sys
import matplotlib.pyplot as plt

name=sys.argv[1]

f=open(name, "r")
data=f.read()
f.close()
data=data.strip().split()

tmp=[]

for i in data:
    tmp.append(float(i))

data=tmp



ffdata=numpy.fft.fft(data)

tmp=[]

for i in range(1,len(ffdata)):
    tmp.append(i/22050)
ffdata=tmp
print(ffdata)

#spektrum=numpy.square(numpy.absolute(erg[1:]))

#plt.plot(freq,erg.real,freq,erg.imag)
#plt.plot(freq,spektrum)

#plt.show()

