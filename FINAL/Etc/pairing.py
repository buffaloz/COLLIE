import sys
import time
import permm
import pexpect
import threading
from neopixel import *

q,w,e,r,t,y=permm.get()
Waiting_second=60
state=1

LED_STRIP = ws.SK6812_STRIP_GRBW
try:
	strip = Adafruit_NeoPixel(q,w,e,r,False,t,y, LED_STRIP)
	strip.begin()

except RuntimeError :
	print "DENIED"
	sys.exit()

def trim(strip):
	global state
	while True :
		strip.setPixelColor(0, Color(10,0,0,0))
		strip.show()
		time.sleep(.2)
		strip.setPixelColor(0, Color(0,0,10,0))
		strip.show()
		time.sleep(.2)
		if state == 2:
			strip.setPixelColor(0, Color(0,10,0,0))
			strip.show()
			print 'DIE'
			break

TR=threading.Thread(target=trim, args=(strip,))
TR.daemon=True
TR.start()

child = pexpect.spawn("bluetoothctl")
child.sendline("discoverable on")
child.expect("Changing")
print "ON"

try:
	child.expect("Paired: yes",timeout=Waiting_second)
	got= (''.join(child.before)).split()
	mac=got[got.index("Device")+y]
	print mac 
	child.sendline("trust {0}".format(mac))
	print "trust comp"
	state=2
	try:
		child.expect("Connected: yes",timeout=Waiting_second)
	except:
		print "error"
except:
	print "error"
finally :
	print "$$final$$"
	child.sendline("quit")

strip.setPixelColor(0, Color(0,0,0,0))
strip.show()
strip.show()
strip.show()
