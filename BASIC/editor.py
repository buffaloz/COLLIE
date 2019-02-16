import os

got=(os.popen("cat /sys/block/mmcblk0/device/serial").readline())[:-1]

f=open("/home/pi/perm.c",'r').readlines()
f.pop(10)
f.insert(10,"        char serial_this[11] = \"%s\";\n"%got)

g=open("/home/pi/perm.c",'w')
g.write(''.join(f))

g.close()

f=open("/home/pi/.asoundrc",'r').readlines()

for i in range(4):
        f.pop(5)

g=open("/home/pi/.asoundrc",'w')
for i in f:
        g.write(i)
g.close()
