import sys

print sys.argv
# Achtung auf shell "'`
print "Anzahl der Kommandozeilenargumente:", len(sys.argv)
for i,a in enumerate(sys.argv):
    print "Arg{}: {}".format(i,a)
