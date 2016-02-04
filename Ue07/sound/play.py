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
import sys, getopt, pyaudio, math, random, subprocess

def make_ramp(f0=30., df=2000., ampl=30000., rate=22050, length=5):       
	
	n = int(rate * length)
	wav = ''
		
	for t in range(0, n):
	
		w = 2 * math.pi * (df / (rate * length) * t + f0) / rate
		#print w /(2 * math.pi)*rate
		f = int(ampl * math.sin(w * t))
		wav += chr(f & 0x00FF) + chr((f & 0xFF00) >> 8)
	
	return wav
	
	
# -------------------------------------
def make_sin(f0=1000.,ampl=30000,rate=22050,length=5.):
  w = 2. * math.pi * f0 / rate              
  n = int(rate * length)
  wav=''
  for i in range(0, n):
    f = int(ampl*math.sin(w*i))
    wav += chr(f & 0x00FF) + chr((f & 0xFF00) >> 8) #auf 8 bit erweitern
  return wav
  
#------------------------------------------
def make_noise(ampl=30000,rate=22050,length=5.):
	wav = ''
	for i in range(0, int(rate*length)):
		f = int(ampl * random.uniform(-1,1))
		wav += chr(f & 0x00FF) + chr((f & 0xFF00) >> 8)
	return wav
#------------------------------------------

if __name__ == '__main__':
	opt=getopt.getopt(sys.argv[1:], "s:f:d:t:a:h")

	rate = 22050
	sound = 'sin'
	freq = 440.
	df = 8000.
	tr = 5.
	ampl = 30000
	for o in opt[0]:
	 if o[0]=='-t': tr=float(o[1])
	 if o[0]=='-s': sound=o[1]
	 if o[0]=='-f': freq=float(o[1])
	 if o[0]=='-d': df=float(o[1])
	 if o[0]=='-a': ampl=float(o[1])
	 if o[0]=='-h': print(__doc__); sys.exit(0)

	type_d={"sin": {"func": make_sin, "args":{"f0":freq,"ampl":ampl,"rate":22050,"length":tr}},
		 "ramp": {"func": make_ramp,"args":{"f0":freq,"df":df,"ampl":ampl,"rate":22050,"length":tr}},
		"noise": {"func": make_noise,"args":{"ampl":ampl,"rate":22050,"length":tr}}}


	wave=type_d[sound]["func"](**type_d[sound]["args"])

PyAudio = pyaudio.PyAudio
p = PyAudio()
stream = p.open(format = p.get_format_from_width(2), 
                channels = 1, 
                rate = rate, 
                output = True)
stream.write(wave)
stream.stop_stream()
stream.close()
p.terminate()
