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
import sys, getopt, pyaudio, multiprocessing, time, make_sound
import numpy as np
import matplotlib.pyplot as plt

#erzeuge datei zum abspielen
def create_sound(type_d):
    return type_d[sound]["func"](**type_d[sound]["args"])

class Play(multiprocessing.process):
    def __init__(self,rate,wav):
        multiprocessing.process.__init__(self)
        self.wav=wav
        self.rate=rate
    def run(self):
        PyAudio = pyaudio.PyAudio
        p = PyAudio()
        stream = p.open(format = p.get_format_from_width(2), 
                    channels = 1, 
                    rate = self.rate, 
                    output = True)
        stream.write(self.wav)
        stream.stop_stream()
        stream.close()
        p.terminate()
        
class Record(multiprocessing.process):
    def __init__(self,rate,RECORD_SECONDS):
        multiprocessing.process.__init__(self)
        self.rate=rate
        self.RECORD_SECONDS=RECORD_SECONDS
    def run(self):
        rate = self.rate
        out_filename='record16'
        RECORD_SECONDS = self.RECORD_SECONDS
        FORMATE = pyaudio.paInt16
        CHUNK_SIZE = 1024
      
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMATE, channels=1, rate=rate, input=True, output=True, frames_per_buffer=CHUNK_SIZE)

        f = open(out_filename, 'w')

        data = ''
        for i in range(int(rate / CHUNK_SIZE * RECORD_SECONDS)):
            data += str(stream.read(CHUNK_SIZE))
    
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        f.write(data)
        f.close()
        return data


if __name__== "__main__":
    
    opt=getopt.getopt(sys.argv[1:], "s:f:d:t:a:h")
    rate = 22050
    sound = 'sin'
    freq = 1000.
    df = 8000.
    tr = 5.
    ampl = 30000
    for o in opt[0]:
        if o[0]=='-t': tr=float(o[1])
        if o[0]=='-s': sound=o[1]
        if o[0]=='-f': freq=float(o[1])
        if o[0]=='-d': df=float(o[1])
        if o[0]=='-a': ampl=float(o[1])
        if o[0]=='-h': print (__doc__); sys.exit(0)
    
    type_d={"sin": {"func": make_sound.make_sin, "args":{"f0":freq,"ampl":ampl,"rate":22050,"length":tr}},
        "ramp": {"func": make_sound.make_ramp,"args":{"f0":freq,"df":df,"ampl":ampl,"rate":22050,"length":tr}},
        "noise": {"func": make_sound.make_noise,"args":{"ampl":ampl,"rate":22050,"length":tr}},
        "square":{"func": make_sound.make_square,"args":{"f0":freq, "ampl":ampl, "rate":22050, "length":tr}},
        "triangle":{"func": make_sound.make_triangle,"args":{"f0":freq, "ampl":ampl, "rate":22050, "length":tr}},
        }
    
    wav=create_sound(type_d)
    Ply=Play
    ply=Ply(rate,wav)
    ply.run()
    
    
    Rec=Record
    rec=Rec(rate,tr)
    wav=rec.run()
    #print(wav)
    while multiprocessing.active_children()>1:
        time.sleep(0.1)

    decoded = np.fromstring(wav, 'Int16')
    f=open("testwav","w")
    for i in decoded:
        f.write(str(int(i))+"\n")
    f.close()
    print(len(decoded))
    wav=wav.strip().split()
    #print(wav)
    #print('lala')
    #print(ord(wav[0][0]))
    tmp=[]
    for i in wav:
        tmp.append(int(i,16))
    data=tmp
    #print(data)
    ffdata=np.fft.fft(data)
    #print(ffdata)
        
    f=[]
    for i in range(1,len(ffdata)):
        f.append(i/rate)
    spec=np.square(np.absolute(ffdata[1:]))
    plt.plot(f,ffdata.real,f,ffdata.imag)
    plt.plot(f,spec)
    plt.show()
        

'''   
class analysis(threading.Thread):
    def __init__(self,data):
        threading.Thread.__init__(self)
        self.data=data
    def run(self):
        rate = 22050
        data=self.data.strip().split()
        print(data)
        print('lala')
        print(ord(data[0][0]))
        tmp=[]
        for i in data:
            tmp.append(float(i))
        data=tmp
        ffdata=np.fft.fft(data)
        #print(ffdata)
        
        f=[]
        for i in range(1,len(ffdata)):
            f.append(i/rate)
        
        spec=np.square(np.absolute(ffdata[1:]))
        plt.plot(f,ffdata.real,f,ffdata.imag)
        plt.plot(f,spec)
        plt.show()
    



'''
#------------------------------------------

