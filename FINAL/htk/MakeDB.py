import os
import os.path
import time
import shutil
import datetime
import new_codetr

config="/home/pi/based_files/config.config"
data_path="/home/pi/based_files/previousDB/data1.mfcc"

#path=raw_input("Enter the previous Trainning path : ")
#======================================================================
c_dic={}
current=[word.strip('\n') for word in os.popen("ls /home/pi").readlines() if word != "wav.py\n"]
maxx=max([len(word) for word in current])

for i in current:
	c_dic[current.index(i)]=i
	print current.index(i),":",
	while len(i) < maxx :
		i+=' '
	print i

try :
	path=c_dic.get(input("Select the path : "))
except SyntaxError : 
	raise ValueError("Choose path correctly")

if path==None :
	print("$$BYE$$")
	raise ValueError("Choose path correctly")

if not os.path.exists("/home/pi/%s/created_prac"%path) :
	print "\n\n"
	c_dic={}
	current=[word.strip('\n') for word in os.popen("ls /home/pi/%s"%path).readlines() if word != "wav.py\n"]
	maxx=max([len(word) for word in current])

	for i in current:
		c_dic[current.index(i)]=i
		print current.index(i),":",
		while len(i) < maxx :
			i+=' '
		print i

	try :
		path="%s/%s"%(path,c_dic.get(input("Select the path : ")))
		print path
	except SyntaxError :
	        raise ValueError("Choose path correctly")

	if path==None :
		print("$$BYE$$")
		raise ValueError("Choose path correctly")
#======================================================================

codetr="%s/created_prac/new.scp"%path

log=open("/home/pi/based_files/previousDB/log",'a')

mfcc=raw_input("Do you have .mfcc file?  : ")

if not (mfcc == 'yes') :
	new_codetr.create_codetr(path)
	os.system("/home/pi/htk/HTKTools/HCopy -T 1 -C %s -S %s"%(config,codetr))

L_st = os.listdir("%s/Left"%path)
R_st = os.listdir("%s/Right"%path)
E_st = os.listdir("%s/Emergency"%path)
G_st = os.listdir("%s/Go"%path)
S_st = os.listdir("%s/Stop"%path)
N_st = os.listdir("%s/Noise"%path)
st_st = [L_st,R_st,E_st,G_st,S_st,N_st]
cmd = ["Left","Right","Emergency","Go","Stop","Noise"]
cnt=0

for i in st_st :
	for j in i :
		while os.path.exists(data_path) :
			cnt += 1
			if len(data_path) == 42 :
				data_path="%s%d.mfcc"%(data_path[:-6],cnt)
			elif len(data_path) == 43 :
				data_path="%s%d.mfcc"%(data_path[:-7],cnt)
			elif len(data_path) == 44 :
				data_path="%s%d.mfcc"%(data_path[:-8],cnt)

		if (j[-5:]==".mfcc") :	
			if j[:-6] in cmd :
				shutil.copy("%s/%s/%s"%(path,j[:-6],j), data_path)
			else : 
				shutil.copy("%s/%s/%s"%(path,j[:-7],j), data_path)

			f=open("/home/pi/based_files/previousDB/train.scp",'a')
			f.write("%s\n"%data_path)
			f.close()

			f=open("/home/pi/based_files/previousDB/words.mlf",'a')
			f.write("\"*%s.lab\"\n"%data_path[31:-5])
			if (j[:-6] == cmd[0]) or (j[:-6] == cmd[1]) or (j[:-6] == cmd[2]) or (j[:-6] == cmd[3]) or (j[:-6] == cmd[4]) or (j[:-6] == cmd[5]) :
				f.write("%s\n"%j[:-6].upper())
			else :
				f.write("%s\n"%j[:-7].upper())
			f.write(".\n")
			f.close()	

			log.write("%s\n"%data_path)

log.write("%s\n"%datetime.datetime.now())
log.write("%s  "%path)
log.write("Copy complete\n")
log.close()

print ("**COMPLETE**")
	

	
