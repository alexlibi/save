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
import sys, getopt, pyaudio, math, random



def make_ramp(f0=30., df=2000., ampl=30000., rate=22050, length=5.):
    n = int(rate * length)
    wav = ''
    #wprev = 0
    for t in range(0, n):
        w = 2 * math.pi * (df / (rate * length) * t + f0) / rate
        #assert w >= wprev
        #wprev = w
        #print(w) # /(2 * math.pi)*rate
        f = int(ampl * math.sin(w * t))
        #assert f >= -32767 and f <= 32767
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
    n=int(rate*length)
    for i in range(0,n):
        f = int(ampl * random.uniform(-1,1))
        wav += chr(f & 0x00FF) + chr((f & 0xFF00) >> 8)
    return wav

def make_square(f0=1000,ampl=30000,rate=22050,length=5.):
    n=int(rate*length)
    tmp=round(rate/f0)
    wav=''
    for i in range(0,n):
        if i%tmp<tmp/2:
            f=ampl
        else:
            f=-ampl
        print(f)
        wav+=chr(f&0x00FF)+chr((f&0x00FF)>>8)
    return wav

def make_triangle(f0=1000,ampl=30000, rate=22050, length=5.):
    n = int(length * rate)
    tmp=round(rate/f0)
    wav=''
    for i in range(0,n):
        if i%tmp<tmp/2:
            f=int(ampl*(1-4*(i%tmp)/tmp))
        else:
            f=int(ampl*(-1+4*((i%tmp)-tmp/2)/tmp))
        print(f)
        wav+=chr(f&0x00FF)+chr((f&0x00FF)>>8)
    return wav

#------------------------------------------

def play_sound(rate,wave):
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
