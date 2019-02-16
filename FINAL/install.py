#-*- coding: utf-8 -*-
import os
import pexpect

htks=['HCopy','HLEd','HCompV','HERest','HHEd','HParse','HVite','HResults']

for i in htks :
	os.system("chmod 777 /home/pi/htk/HTKTools/%s"%i) #HTK 툴의 사용권한 및 실행여부 변경

os.chdir("/home/pi/rpi_ws281x/python") #LED_Strip 제어용 모듈 경로복사
os.system("sudo python setup.py install") #LED_Strip 제어용 모듈의 파이썬 모듈화

os.system("sudo mv /home/pi/rpi_ws281x /home/pi/Etc") #Etc폴더로 이동
os.system("sudo mv /home/pi/mic_hat /home/pi/Etc") #Etc폴더로 이동
os.system("sudo mv /home/pi/seeed-voicecard /home/pi/Etc") #Etc폴더로 이동
os.system("sudo rm /home/pi/install.sh") #파일 삭제
os.system("sudo rm /home/pi/README.md") #파일 삭제

os.system("sudo rm -rf /home/pi/build") #/home/pi의 build폴더 삭제
os.system("sudo rm -rf /home/pi/gadget") #/home/pi의 build폴더 삭제

child=pexpect.spawn('bluetoothctl')
child.sendline('remove 00:F4:6F:80:8C:FE')
child.expect('removed')

print "EVERYTHING DONE!!"
os.system("sudo rm /home/pi/install.py") #파일 삭제
