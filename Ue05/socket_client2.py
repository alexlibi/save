import socket, sys


port = int(sys.argv[2])
host = sys.argv[1]

#data = "test" * 10485760                  # 40MB of data
data = "test"
#data = "test" *4094

# Senden und empfangen einer goesseren Datenmenge in chunks von z.B. 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

byteswritten = 0
while byteswritten < len(data):
    startpos = byteswritten
    endpos = min(byteswritten + 1024, len(data))
    byteswritten += s.send(data[startpos:endpos])
    sys.stdout.write("Wrote %d bytes\n" % byteswritten)
    sys.stdout.flush()
    
s.shutdown(1)

print "All data sent."
sys.stdout.flush()

while 1:
    buf = s.recv(1024)
    if not len(buf):
        break
    sys.stdout.write(buf)
    sys.stdout.flush()

