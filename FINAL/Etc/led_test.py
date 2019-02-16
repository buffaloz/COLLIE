import os
import sys
import permm
import time
import argparse
import threading
import RPi.GPIO as gpio
from neopixel import *
from multiprocessing import Process
#===================================================================
#LED_STRIP = ws.WS2811_STRIP_GRB  # Strip type and colour ordering
LED_STRIP = ws.SK6812_STRIP_GRBW 
#===================================================================
cmd_list = [' ','LEFT','RIGHT','EMERGENCY','GO','STOP']
#===================================================================
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

def colorWipe_GO(strip, color, wait_ms):
	"""Wipe color across display a pixel at a time."""
	for i in range(11):
		strip.setPixelColor(i, color)
		strip.setPixelColor(i-1, Color(100-(i*20),100-(i*20),100-(i*20)))
		strip.setPixelColor(i+11, color)
		strip.setPixelColor(i+10, Color(100-(i*20),100-(i*20),100-(i*20)))
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

def Led_GO(fron, strip, color, wait_ms):
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

def Led_GO_R(fron, strip, color, wait_ms):
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

def Led_OFF(fron, to, strip, wait_ms):
	for i in range(fron,to):
		strip.setPixelColor(i, Color(0,0,0))
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
#===================================================================
def main() :
	dic={1:"LEFT", 2:"RIGHT", 3:"EMERGENCY", 4:"GO", 5:"STOP", 6:"ETC"}
	parser = argparse.ArgumentParser()
	parser.add_argument('X',type=int)

	args = parser.parse_args()
	dir = dic.get(args.X)

	q,w,e,r,t,y=permm.get()

	try:
		strip = Adafruit_NeoPixel(q,w,e,r,False,t,y, LED_STRIP)
		strip.begin()

	except RuntimeError :
		print "DENIED"
		sys.exit()

	if "LEFT" in dir :
		for i in range(7) :	
			Tongue_L(0,10,strip, Color(1, 70, 4,0),15) 
			time.sleep(.3)

	elif 'RIGHT' in dir :
		for i in range(7) :	
			Tongue(10,20,strip, Color(1, 70, 4,0),15) 
			time.sleep(.3)

	elif 'EMERGENCY' in dir :
		for i in range(20) :
			Led_ON(0, 20, strip, Color(50,50,0), 70)
			Led_OFF(0, 20, strip, 100)
  
	elif 'GO' in dir :
		for i in range(23) :
			Led_GO(i, strip, Color(100,100,100),100)
		for i in range(19,-3,-1) :
			Led_GO_R(i, strip, Color(100,100,100),100)
		Led_OFF(0, 22, strip, 10)
  
  	elif 'STOP' in dir :
		for i in range(6) :	
			colorWipe_ST(strip, Color(150, 0, 0), 35)  # Red wipe
			time.sleep(0.5)	
			colorWipe_ST(strip, Color(0, 0, 0), 35)  # Red wipe
	elif 'ETC' in dir :
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
		time.sleep(2)
		Led_OFF(0,22,strip,100)
	else :
		print("Again") 

if __name__ == '__main__' :
	main()

