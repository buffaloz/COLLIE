sudo apt-get install python-alsaaudio -y #파이썬 음성녹음 모듈 설치
sudo apt-get install python-spidev -y #리스피커 RGB_LED 제어용 SPI통신 모듈 설치
sudo apt-get install python-numpy -y #파이썬 계산 모듈 설치
sudo apt-get install python-dbus python-pexpect -y #파이썬 DBUS, pexpect 모듈 설치

sudo mv /home/pi/hcopy.so /usr/lib/python2.7/dist-packages #hcopy모듈을 파이썬 라이브러리로 이동
sudo mv /home/pi/hvite.so /usr/lib/python2.7/dist-packages #hvite모듈을 파이썬 라이브러리로 이동

sudo apt-get install python-setuptools build-essential python-dev scons swig -y #scons, swig 설치 
git clone https://github.com/jgarff/rpi_ws281x.git #LED_Strip 제어용 모듈 깃허브 복사
git clone https://github.com/respeaker/mic_hat.git #리스피커 RGB_LED 제어용 모듈 깃허브 복사
scons -C /home/pi/rpi_ws281x/ #LED_Strip 제어용 모듈 설치
 
mkdir /home/pi/workspace1 #폴더 생성
mkdir /home/pi/result #폴더 

python /home/pi/install.py #install 2단계 실행
