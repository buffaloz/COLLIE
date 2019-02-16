import os
import sys
import like
import time
import wave
import pixels
import permm
import numpy
import ctypes
import Queue
import hcopy
import hvite
import alsaaudio
import RPi.GPIO as GPIO
from neopixel import *
from multiprocessing import Process, Manager
from multiprocessing import Queue as Multi_queue 
#=================================================================================
THRESHOLD=1500
WAVE_OUTPUT="/home/pi/workspace1/file1.wav"
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN,GPIO.PUD_DOWN)
GPIO.setup(5, GPIO.IN,GPIO.PUD_DOWN)
GPIO.setup(6, GPIO.IN,GPIO.PUD_DOWN)

q,w,e,r,t,y=permm.get()

LED_STRIP = ws.SK6812_STRIP_GRBW 

try:
	strip = Adafruit_NeoPixel(q,w,e,r,False,t,y, LED_STRIP)
	strip.begin()

except RuntimeError : 
	print "DENIED"
	sys.exit()

AT = -9999
RT_L,RT_R,RT_E,RT_G,RT_S,RT_N = 0,0,0,0,0,0
count, final_state = 0,0
#=================================================================================
def colorWipe(fron, to, strip, color, wait_ms):
	"""Wipe color across display a pixel at a time."""
	for i in range(fron,to):
		strip.setPixelColor(i, color)
		strip.show()
		time.sleep(wait_ms/1000.0)

def colorWipe_ST(strip, color, wait_ms):
	"""Wipe color across display a pixel at a time."""
	for i in range(10):
		strip.setPixelColor(9-i, color)
		strip.setPixelColor(i+10, color)
		strip.show()
		time.sleep(wait_ms/1000.0)

def Tongue(fron, to, strip, color, wait_ms):
	for i in range(fron,to):
		strip.setPixelColor(i, color)
		strip.show()
		time.sleep(wait_ms/1000.0)
	for i in range(to,fron-1,-1):
		strip.setPixelColor(i, Color(0,0,0,0))
		strip.show()
		time.sleep(wait_ms/1000.0)

def Tongue_L(fron, to, strip, color, wait_ms):
	for i in range(to-1,fron-1,-1):
		strip.setPixelColor(i, color)
		strip.show()
		time.sleep(wait_ms/1000.0)
	for i in range(fron,to):
		strip.setPixelColor(i, Color(0,0,0,0))
		strip.show()
		time.sleep(wait_ms/1000.0)

def Led_ON(fron, to, strip, color, wait_ms):
	for i in range(fron,to):
		strip.setPixelColor(i, color)
	strip.show()
	time.sleep(wait_ms/1000.0)

def Led_OFF(fron, to, strip, wait_ms):
	for i in range(fron,to):
		strip.setPixelColor(i, Color(0,0,0))
	strip.show()
	time.sleep(wait_ms/1000.0)

def Led_GO(fron, strip, wait_ms):
	if fron < 20 :
        		strip.setPixelColor(fron-3, Color(0,0,0,0))
        		strip.setPixelColor(fron-2, Color(0,0,0,10))
        		strip.setPixelColor(fron-1, Color(0,0,0,50))
        		strip.setPixelColor(fron, Color(0,0,0,100))
	elif fron == 20 :
		strip.setPixelColor(19, Color(0,0,0,100))
		strip.setPixelColor(18, Color(0,0,0,10))
		strip.setPixelColor(17, Color(0,0,0,0))
	elif fron == 21 :
		strip.setPixelColor(19, Color(0,0,0,100))
		strip.setPixelColor(18, Color(0,0,0,0))
	strip.show()
	time.sleep(wait_ms/1000.0)

def Led_GO_R(fron, strip, wait_ms):
	if fron > -1 :
		strip.setPixelColor(fron+3, Color(0,0,0,0))
		strip.setPixelColor(fron+2, Color(0,0,0,10))
		strip.setPixelColor(fron+1, Color(0,0,0,50))
		strip.setPixelColor(fron, Color(0,0,0,100))
	elif fron == -1 :
		strip.setPixelColor(0, Color(0,0,0,100))
		strip.setPixelColor(1, Color(0,0,0,10))
		strip.setPixelColor(2, Color(0,0,0,0))
	elif fron == -2 :
		strip.setPixelColor(0, Color(0,0,0,100))
		strip.setPixelColor(1, Color(0,0,0,0))
	strip.show()
	time.sleep(wait_ms/1000.0)

def Rainbow(fron, to , strip, wait_ms,r,g,b):
	for i in range(fron, to):
		strip.setPixelColor(9-i, Color(r,g,b))
		strip.setPixelColor(i+10, Color(r,g,b))
		if i>0: 
			strip.setPixelColor(10-i, Color(0,0,0))
			strip.setPixelColor(i+9, Color(0,0,0))
		strip.show()
	time.sleep(wait_ms/1000.0)
#=================================================================================
def led(q,starter):
	dir=""
	cnt=0
	Gstate=0

	print("$$Process start$$")
	present = time.time()

	while True:
		if starter.value :
			dir=q.get()	
			starter.value=False

		if "LEFT" in dir :
			Tongue_L(0,10,strip, Color(1, 60, 4,0),15) 
			time.sleep(.3)

		elif 'RIGHT' in dir :
			Tongue(10,20,strip, Color(1, 60, 4,0),15) 
			time.sleep(.3)
	
		elif 'EMERGENCY' in dir :
			Led_ON(0, 20, strip, Color(50,50,0), 70)
			Led_OFF(0, 20, strip, 100)
  	
		elif 'GO' in dir :
			if Gstate==0:
				for i in range(23) :
       	         			Led_GO(i, strip,100)
				Gstate=1
			elif Gstate==1:
				for i in range(19,-3,-1) :
                			Led_GO_R(i, strip,100)
				Gstate=0
			Led_OFF(0,20,strip,1)
  	
		elif 'STOP' in dir :
			colorWipe_ST(strip, Color(150, 0, 0), 35)  # Red wipe
			time.sleep(0.5)	
			colorWipe_ST(strip, Color(0, 0, 0, 0), 35)  # Red wipe

		elif 'NOISE' in dir:
			q.put('')
			starter.value=True

		elif 'break' in dir:
			print("$$Process down$$")
			break
		else : 
			time.sleep(0.1)
#=================================================================================
def Likelyhood(dir,L1,L2):
	L1=int(L1)
	L2=int(L2)
	dic_RT={"LEFT":RT_L,"RIGHT":RT_R,"EMERGENCY":RT_E,"GO":RT_G,"STOP":RT_S,"NOISE":RT_N}
	
	if L1 > AT :
		if (L1-L2) > dic_RT[dir] :
			print "Result : "+dir
			q.put(dir)
			starter.value=True

		else : 
			print "$$Relatively Again$$"
			Led_ON(0, 22, strip, Color(0,0,100), 100)
			Led_OFF(0, 22, strip, 100)
			Led_ON(0, 22, strip, Color(0,0,100), 100)
			Led_OFF(0, 22, strip, 100)

	else : 
		print "$$Absolutely Again$$"
		Led_ON(0, 22, strip, Color(0,0,100), 100)
		Led_OFF(0, 22, strip, 100)
		Led_ON(0, 22, strip, Color(0,0,100), 100)
		Led_OFF(0, 22, strip, 100)	
#=================================================================================
def VR(arg):
	hcopy.mfcc('')
	hvite.Nbest('')
	dir,L1,L2,L3,L4,L5,L6=like.result()
	Likelyhood(dir,L1,L2)
	pixels.State(1)
	print("Rec")
#=================================================================================
def Z(Gstate):
	if Gstate==0:
		for i in range(23) :
			Led_GO(i, strip,100)
	elif Gstate==1:
		for i in range(19,-3,-1) :
			Led_GO_R(i, strip,100)	
	Led_OFF(0,20,strip,1)
#=================================================================================
def main(q,starter) :
	global emgc
	emgc_pre=0
	frames=[]
	check=0
	current_w=0
	present = time.time()
	raptime = 0 
	a,b,c,d,e = 0,0,0,0,0
	count,final_state = 0,0
	buttonState = GPIO.input(6)
	buttonState_respeaker = GPIO.input(17)

	Led_ON(0, 22, strip, Color(0,50,0), 70)
	Led_OFF(0, 22, strip, 100)
	Led_ON(0, 22, strip, Color(0,50,0), 70)
	Led_OFF(0, 22, strip, 100)
	pixels.State(1)

	print("Rec")

	while 1:
		buttonState_respeaker = GPIO.input(17)

		if e==0:
			vr=Process(target=VR, args=(1,))
			
			time.sleep(.2)
			inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE)
			inp.setchannels(1)
			inp.setrate(26000)
			inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
			inp.setperiodsize(1024)
			print("Rec")
			time.sleep(.5)
			e=1

		current = time.time()
		timeout = float("%.1f"%(current-present))
	
		l, data = inp.read()
		try : 
			data1 = numpy.fromstring(data, dtype='int16')
		except : 
			print 'error'
			l, data = inp.read()
			data1 = numpy.fromstring(data, dtype='int16')

		top=numpy.abs(data1).mean()
	
		if top<5:
			q.put("NOISE")
			starter.value=True
			emgc=1
			break
		else :
			emgc=0

		if timeout%0.5 == 0.0:
		#Reset frame buffer every 0.5 second#
			a += 1
			if a == 1 :
				frames=[]	
		else :
			a=0
			frames.append(data)
			if top>THRESHOLD :
				pixels.State(2)
				print timeout

				while raptime < 0.6 :
					l, data = inp.read()
					frames.append(data)
					raptime=float("%.2f"%(time.time()-current))
					time.sleep(0.1)
		
				w = wave.open(WAVE_OUTPUT, 'wb')
				w.setnchannels(1)
				w.setsampwidth(2)
				w.setframerate(26000)
				w.writeframes(b''.join(frames))
				w.close()
				frames=[]
				print("comp")
				vr.start()
				raptime=0
				e=0

		time.sleep(0.1)
		while not buttonState_respeaker :
			time.sleep(.1)

			l, data = inp.read()
			data1 = numpy.fromstring(data, dtype='int16')
			top=numpy.abs(data1).mean()

			buttonState_respeaker = GPIO.input(17)
			count += 1
			print "push"

			if count > 0 :
				q.put("NOISE")
				starter.value=True
				final_state=1
				for i in range(5) :
					Led_ON(0, 22, strip, Color(50,0,0), 70)
					Led_OFF(0, 22, strip, 100)
				pixels.State(3)
				break
		count=0
		if final_state == 1 :
			break
	print("end")
	e=0
#=================================================================================
if __name__ == '__main__':
	pixels.State(3)
	dlfeks1,dlfeks2,dlfeks3 = 0,0,0
	global emgc
	global buttonState
	q=Multi_queue()
	mm=Manager()
	starter=mm.Value(ctypes.c_bool, False)

	Led=Process(target=led, args=(q,starter))
	Led.daemon = True
	Led.start()

	present=time.time()
	Gstate=0
	emgc=0

	while y:
		current=time.time()
		timeout=float("%.1f"%(current-present))

		if timeout%5.0 < 0.15 :
			if Gstate==0:	
				Gstate=1
			elif Gstate==1:
				Gstate=0
			kit=Process(target=Z, args=(Gstate,))
			kit.start()
	
		buttonState=GPIO.input(17)+1

		if emgc == 1 :
			buttonState=1
		if buttonState == 1 :
			print "PUSH"
			emgc = 0
			dlfeks1 = 0
			dlfeks3 += 1
			if dlfeks3 == 1 :
				main(q,starter)
				if emgc == 1 :
					dlfeks3=0
			if dlfeks3 == 17 :
				Rainbow(0,10,strip,40,100,0,0)
				Rainbow(0,9,strip,40,100,50,0)
				Rainbow(0,8,strip,40,100,100,0)
				Rainbow(0,7,strip,40,0,100,0)
				Rainbow(0,6,strip,40,0,0,100)
				Rainbow(0,5,strip,40,10,10,100)
				Rainbow(0,4,strip,40,100,0,100)
				Rainbow(0,3,strip,40,100,100,100)
				Rainbow(0,2,strip,40,0,100,100)
				Rainbow(0,1,strip,40,50,50,100)
				time.sleep(0.5)
				Led_OFF(0,22,strip,100)

				q.put("break")
				starter.value=True
				os.system("python /home/pi/htk/Trainning_sw.py")

				Rainbow(0,10,strip,40,100,0,0)
				Rainbow(0,9,strip,40,100,50,0)
				Rainbow(0,8,strip,40,100,100,0)
				Rainbow(0,7,strip,40,0,100,0)
				Rainbow(0,6,strip,40,0,0,100)
				Rainbow(0,5,strip,40,10,10,100)
				Rainbow(0,4,strip,40,100,0,100)
				Rainbow(0,3,strip,40,100,100,100)
				Rainbow(0,2,strip,40,0,100,100)
				Rainbow(0,1,strip,40,50,50,100)
				time.sleep(0.5)
				Led_OFF(0,22,strip,100)

				Led=Process(target=led, args=(q,starter))
				Led.daemon = True
				Led.start()
			
		else :	
			dlfeks1 += 1
			dlfeks2 = 0
			dlfeks3 = 0
			if dlfeks1 == 1 :
				print("$$OFF$$")
				time.sleep(0.2)
		time.sleep(0.2)
	print "DENIED"
#=================================================================================
