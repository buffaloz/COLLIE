import os
import os.path
import pexpect
import time

L = '/home/pi/result/LEFT.txt'
R = '/home/pi/result/RIGHT.txt'
E = '/home/pi/result/EMERGENCY.txt'
G = '/home/pi/result/GO.txt'
S = '/home/pi/result/STOP.txt'

result="/home/pi/result/recout1.mlf"
end="/home/pi/result/end"

os.system('sudo rm %s'%result)

cmd = {'LEFT':'Left','RIGHT':'Right','EMERGENCY':'Emergency','GO':'Go','STOP':'Stop'}

while True :
	time.sleep(.2)
	if os.path.exists(result):
		f=open("/home/pi/result/recout1.mlf",'r').readlines()
		while f == [] : 
			f=open("/home/pi/result/recout1.mlf",'r').readlines()
		word=(f[3].split())[2]

		os.system('aplay /home/pi/Etc/%s.wav'%cmd.get(word))
		os.system('sudo rm %s'%result)

	if os.path.exists(end):
		os.system('sudo rm %s'%end)
		print ("BYE")
		break
