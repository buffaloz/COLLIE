import time
import wave
import permm
import alsaaudio
import RPi.GPIO as GPIO
from neopixel import *

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

def Led_NUM(num,strip,color):
	for i in range(0,num*2):
		strip.setPixelColor(i+10,color*15)
		strip.setPixelColor(9-i,color*15)
	strip.show()

def number(cmd,num,strip,shrdma):
	tnstj=["Noise","Left","Right","Emergency","Go","Stop","End"]
	dic = {"Left":Color(3,0,0,0), "Right":Color(3,1,0,0), "Emergency":Color(3,3,0,0), "Go":Color(0,3,0,0), "Stop":Color(0,0,3,0), "Noise":Color(3,0,3,0),"End":Color(0,0,0,0)}
	plus=dic.get(cmd)
	
	Led_ON(0,20,strip,plus,0)
	Led_NUM(num,strip,plus)
	if num%shrdma == 0 :
		plus=dic.get(tnstj[tnstj.index(cmd)+1])
		time.sleep(1)
		Led_OFF(0,22,strip,50)
		Led_ON(0,20,strip,plus,0)

def rec(path,shrdma) :
	LED_STRIP = ws.SK6812_STRIP_GRBW 
	q,w,e,r,t,y=permm.get()
	try:
		strip = Adafruit_NeoPixel(q,w,e,r,False,t,y, LED_STRIP)
		strip.begin()

	except RuntimeError :
		print "DENIED"
		sys.exit()

	Led_ON(0,20,strip,Color(3,0,3,0),0)

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(17, GPIO.IN,GPIO.PUD_DOWN)

	RECORD_SECONDS = 0.7
	cmd = ""
	numL,numR,numE,numG,numS,numN = 0,0,0,0,0,0
	code=[]
	push=0
	cnt=0
	cntt=0
	start=-1
	check=-1
	#shrdma=5 #The number of recording

	while True :
		if cntt == 0:
			cntt += 1
		if cntt == 1:
			cntt = 2
			inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE)
			inp.setchannels(1)
			inp.setrate(26000)
			inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
			inp.setperiodsize(1024)
			print ("|1 : Left|2 : Right|3 : Emergency|4 : Go |5 : Stop|6 : Noise|7 : End|")
			print ("|cnt : %d |cnt : %d  |cnt : %d      |cnt : %d|cnt: %d  |cnt : %d  |"%(numL,numR,numE,numG,numS,numN))
		
		got=GPIO.input(17)
		if got == 1:
			cnt += 1
			if cnt == 1:
				start+=got
				check += 1
				print start
		else :
			cnt=0

		if check == 1 :
			if ((start-1)//shrdma) == 1 :
				Led_OFF(0,22,strip,1)
				cmd = "Left"
				numL+=1
				WAVE_OUTPUT_FILENAME = path%(cmd,cmd,numL)

			elif (start-1)//shrdma == 2 :
				Led_OFF(0,22,strip,1)
				cmd = "Right"
				numR+=1
				WAVE_OUTPUT_FILENAME = path%(cmd,cmd,numR)
	
			elif (start-1)//shrdma == 3 :
				Led_OFF(0,22,strip,1)
				cmd = "Emergency"
				numE+=1
				WAVE_OUTPUT_FILENAME = path%(cmd,cmd,numE)
	
			elif (start-1)//shrdma == 4 :
				Led_OFF(0,22,strip,1)
				cmd = "Go"
				numG+=1
				WAVE_OUTPUT_FILENAME = path%(cmd,cmd,numG)
	
			elif (start-1)//shrdma == 5 :
				Led_OFF(0,22,strip,1)
				cmd = "Stop"
				numS+=1
				WAVE_OUTPUT_FILENAME = path%(cmd,cmd,numS)
	
			elif (start-1)//shrdma == 0 :
				Led_OFF(0,22,strip,1)
				cmd = "Noise"
				numN+=1
				WAVE_OUTPUT_FILENAME = path%(cmd,cmd,numN)
	
			else : 	
				break
	
			# start Recording
			print ("recording...")
			frames = []
	
			for i in range(0, int(26000 / 1024 * RECORD_SECONDS)):
				l, data = inp.read()
				frames.append(data)
			print ("finished recording")
			print("")
	
			# stop Recording
			waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
			waveFile.setnchannels(1)
			waveFile.setsampwidth(2)
			waveFile.setframerate(26000)
			waveFile.writeframes(b''.join(frames))
			waveFile.close()

			all=numL+numR+numE+numG+numS+numN-1	
			number(cmd,(all%shrdma)+1,strip,shrdma)
	
			code.append(WAVE_OUTPUT_FILENAME)
			check, cntt = 0, 0
	
	return code,numS

if __name__ == "__main__" :
	rec("/home/pi/trainning/%s/%s%d.wav",5)
