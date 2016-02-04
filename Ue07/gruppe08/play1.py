"""Usage: play.py -t # [-h]
            -s sin|ramp|noise play either a sinus or a ramp or noise
            -t # Time in seconds to be played (default: 5)
            -f # Frequency in Hz (default: 440)
            -d # Frequency range for ramp (default: 8000)
            -a # Amplitude (default: 30000)
            -h: Print this help message
  RESULT:
   Play a sound t seconds at your default sound card.
   With a sample rate of 22050 Hz in format S16LE (16 bit int little endian)  
"""
import sys
import time
import getopt
import alsaaudio
from math import *
from getopt import *
from random import *
import random

def make_ramp(f0=30.,df=2000., ampl=30000., rate=22050,length=5):
  # Zu Programmieren
	n=int(rate*length)
	
	wav=''
	for i in range(0,n):
		f=int((i%f0)*df*ampl)
		wav+=chr(f&0x00FF)+chr((f&0xFF00)>>8)
	return wav


def make_rechteck(f0=5.,ampl=30000., rate=22050, length=5):
	n=int(rate*length)
	a=2.*pi*f0/rate
	help1=round(rate/f0)
	print(help1)
	wav=''
	for i in range(0,n):
	
		if i%help1<help1/2.:
			help2=1
		else: help2=0
		f=int(help2*ampl)
		wav+=chr(f&0x00FF)+chr((f&0x00FF)>>8)
	return wav
#--------------
def make_triangle(f0=30., ampl=30000., rate=22050, length=5):
	n=int(rate*length)
	help1=rate/f0
	print(help1)
	wav=''
	for i in range(0,n):
		if i%help1<help1/float(2):
			f=int(i%help1*ampl*2)
		else:
			f=int(ampl-(i/2)%help1)
		wav+=chr(f&0x00FF)+chr((f&0x00FF)>>8)
	return wav
  #------------------------------------
def make_sin(f0=1000.,ampl=30000,rate=22050,length=5.):
  a = 2. * pi * f0/rate              
  n = int(rate * length)
  wav=''
  for i in range(0, n):
    f = int(ampl*sin(a*i))
    wav += chr(f & 0x00FF) + chr((f & 0xFF00) >> 8)
  return wav
# ------------------------------------------
def make_noise(ampl=30000,rate=22050,length=5.):
	n=int(rate*length)
	wav=''
	for i in range(0,n):
		f=int(ampl*random.random())
		wav+=chr(f&0x00FF)+chr((f&0xFF00)>>8)
	return wav
  # Zu Programmieren 
# ------------------------------------------

if __name__ == '__main__':
  opt=getopt(sys.argv[1:], "s:f:d:t:a:h")

  rate = 22050
  crd = 'default'
  sound= 'sin'
  freq=1000.
  df=8000.
  tr=10.
  ampl=30000
  for o in opt[0]:
     if o[0]=='-t': tr=float(o[1])
     if o[0]=='-s': sound=o[1]
     if o[0]=='-f': freq=float(o[1])
     if o[0]=='-d': df=float(o[1])
     if o[0]=='-a': ampl=float(o[1])
     if o[0]=='-h': print(__doc__); sys.exit(0)

  type_d={"sin": {"func": make_sin, "args":{"f0":freq,"ampl":ampl,"rate":22050,"length":tr}},
         "ramp": {"func": make_ramp,"args":{"f0":freq,"df":df,"ampl":ampl,"rate":22050,"length":tr}},
        "noise": {"func": make_noise,"args":{"ampl":ampl,"rate":22050,"length":tr}},
		"recht": {"func":make_rechteck, "args":{"f0":freq,"ampl":ampl, "rate":22050,"length":tr}}, 
		"triangle": {"func": make_triangle, "args":{"f0":freq, "ampl":ampl,"rate":22050, "length":tr}}}


  wave=type_d[sound]["func"](**type_d[sound]["args"])

  # Open the device in playback mode. 
  out = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, card=crd)
  # Set attributes: Mono, 44100 Hz, 16 bit little endian frames
  out.setchannels(1)
  out.setrate(rate)
  out.setformat(alsaaudio.PCM_FORMAT_S16_LE)
  out.setperiodsize(160)

  i = 0
  l= len(wave)
  while i < l:
       i+=2*out.write(wave[i:i+320])








