import sys,string,socket

if len(sys.argv) != 4:
   print  "Usage: %s host port message" % sys.argv[0]
   sys.exit(0)
# Schreibt Nachricht zu einem socket und wartet auf Antwort
host = sys.argv[1]
port = string.atoi(sys.argv[2])
message = sys.argv[3]

# Oeffnen des Sockets
# Auch der client muss einen socket oeffnen
try:
   s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
except socket.error, msg:
   s = None
try:
   s.connect((host,port)) # Verbinden
except socket.error, msg:
   s.close()
   s = None
if s is None:
   print 'Can not open socket ',msg
   sys.exit(1)

# senden der daten
s.send(message+"\r\n")
# lesen der Antwort
data = s.recv(4096)
s.close()
#print 'Received', `data`
#print data
print 'Received:\n', data




