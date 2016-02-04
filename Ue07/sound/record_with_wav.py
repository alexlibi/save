"""Usage: record.py -t # [-h]
            -t #: Time in seconds to be recorded (default: 2)
              -h: Print this help message
     -o filename: Write output to filename.raw and filename.dat (default: record16)
  RESULT:
   Records t seconds from your default sound card.
   With a sample rate of 22050 Hz in format S16LE (16 bit int little endian)  
"""
import sys, time, getopt, math, getopt, pyaudio, wave

if __name__ == '__main__':
  opt=getopt.getopt(sys.argv[1:], "t:o:h")

  RATE = 44100#22050
  out_filename='record16.wav'
  RECORD_SECONDS = 10.
  FORMATE = pyaudio.paInt16
  CHUNK_SIZE = 1024
  
  for o in opt[0]:
     if o[0]=='-t': RECORD_SECONDS=float(o[1])
     if o[0]=='-o': out_filename=o[1]
     if o[0]=='-h': print __doc__; sys.exit(0)

p = pyaudio.PyAudio()
stream = p.open(format=FORMATE, channels=1, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK_SIZE)


wavefile = wave.open(out_filename,'wb')
wavefile.setnchannels(1)
wavefile.setsampwidth(p.get_sample_size(pyaudio.paInt16))
wavefile.setframerate(RATE)


for i in range(int(RATE / CHUNK_SIZE * RECORD_SECONDS)):
    data = stream.read(CHUNK_SIZE)
    wavefile.writeframes(data)

wavefile.close()
stream.stop_stream()
stream.close()
samplew=p.get_sample_size(pyaudio.paInt16)
p.terminate()


#f = open(out_filename, 'w')
#f.write("%s" % data)
#f.close()









