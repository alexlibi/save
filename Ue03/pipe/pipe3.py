from subprocess import *

#    output=`dmesg | grep sda`
#    output=`ps aux | grep pipe3.py`

p1 = Popen(["ps", "aux"], stdout=PIPE)
p2 = Popen(["grep", "pipe3.py"], stdin=p1.stdout, stdout=PIPE, stderr=PIPE)
sout,serr = p2.communicate()
print "result:",sout
print "error:",serr

