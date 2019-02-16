sudo apt-get update
sudo apt-get install python-dev -y
#패키지 리스트 업데이트 후 파이썬 모듈화용 패키지 설치

sudo mkdir /usr/lib/python2.7/test/test
#커스텀 라이브러리 폴더 생성

export PYTHONPATH=$PATHONPATH:/usr/lib/python2.7/test/test
#파이썬 환경변수 설정

python editor.py
#시리얼넘버 확인해서 perm.c에 변수값에 넣고 저장

sudo python setup.py install
#perm.c를 파이썬 모듈화

sudo mv /usr/local/lib/python2.7/dist-packages/perm.so /usr/lib/python2.7/test/test
#만들어진 파이썬 모듈을 커스텀 라이브러리 폴더로 이동

#sudo mv permm.pyc /usr/lib/python2.7/test/test
sudo mv permm.pyc /usr/lib/python2.7/lib-dynload/
#보안 스크립트를 커스텀 라이브러리 폴더로 이동

sudo rm -rf build
#build 폴더 삭제

sudo rm test.wav test.sh README.md
#기타 파일 삭제

sudo rm perm.c permm.py editor.py setup.py setting.sh
#기타 설정파일 삭제
