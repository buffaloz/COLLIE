import os
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN,GPIO.PUD_DOWN)

button=GPIO.input(17)
print "ready"
time.sleep(0.2)

if not button :
	os.system("sudo python /home/pi/Etc/pairing.py")

os.system("sh /home/pi/starter.sh &")
print "$ $ $ $ $ END $ $ $ $ $"
