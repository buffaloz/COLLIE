import time
import os
import os.path
import Rec_tra
import create
from shutil import copyfile, copytree

final		   = "/home/pi/workspace2/trainning"
trainning_path     = "/home/pi/trainning"
based_path	   = "/home/pi/based_files"
config 		   = "/home/pi/based_files/config.config"
config1		   = "/home/pi/based_files/config1.config"
config2		   = "/home/pi/based_files/config2.config"
i = 0

trainning_path=create.directory(trainning_path)

os.system("mkdir %s"%trainning_path)
cmd1_path="%s/Left"%trainning_path
cmd2_path="%s/Right"%trainning_path
cmd3_path="%s/Emergency"%trainning_path
cmd4_path="%s/Go"%trainning_path
cmd5_path="%s/Stop"%trainning_path
cmd6_path="%s/Noise"%trainning_path

path		 = trainning_path+"/%s/%s%d.wav"
created_path     = trainning_path+"/created_prac"
codetr  	 = created_path+"/codetr.scp"
train   	 = created_path+"/train.scp"
words   	 = created_path+"/words.mlf"
proto   	 = based_path+'/proto.txt'
proto_new	 = created_path+'/hmm0/proto'
vFloors 	 = created_path+'/hmm0/vFloors'
diction      = based_path+"/diction.txt"
hmm          = created_path+'/hmm'
monophones   = created_path+'/monophones'
triphones    = created_path+'/triphones'
phone0       = created_path+'/phone0.mlf'

p=os.system("mkdir %s"%created_path)
p=os.system("mkdir %s"%cmd1_path)
p=os.system("mkdir %s"%cmd2_path)
p=os.system("mkdir %s"%cmd3_path)
p=os.system("mkdir %s"%cmd4_path)
p=os.system("mkdir %s"%cmd5_path)
p=os.system("mkdir %s"%cmd6_path)
print("Successfully made - trainning folder")

time.sleep(1.5)
 
code=["Hello"]
print("...Ready to Rec...")
print("")

code,num=Rec_tra.rec(path) #Recoding and get .wav's directory
time.sleep(1)

create.codetr(codetr,code)
create.train(train,code)
create.words(words,code,trainning_path)
create.monophones(diction,created_path)
create.mkdir_hmm(created_path)
print("")

while True:

	print ("|1:Trainning|0:End|")
	try :
		flow=int(input('start:'))
	except SyntaxError :
		flow=2

	if flow==1 :
		p=os.system("/home/pi/htk/HTKTools/HCopy -T 1 -C %s -S %s"%(config,codetr))
		time.sleep(1)
		comp="1."
		print ("%s step. complete"%comp)

	#elif flow==2 :
		p=os.system("/home/pi/htk/HTKTools/HLEd -l '*' -d %s/diction.txt -i %s/phone0.mlf %s/mkphones0.led %s/words.mlf"%(based_path,created_path,based_path,created_path))
		time.sleep(1)
		if (os.path.exists("%s/phone0.mlf"%created_path)) :
			print("**HLEd Complete**")
			print("")
			comp += "2."
		else : create.error("HLEd error")
		print ("%s step. complete"%comp)

	#elif flow==3 :
		p=os.system("/home/pi/htk/HTKTools/HCompV -C %s -f 0.01 -m -S %s -M %s %s"%(config1,train,hmm+'0',proto))
		time.sleep(1)
		if (os.path.exists("%s"%vFloors)) :
			print("**HCompV Complete**")
			print("")
			comp += "3."
		else : create.error("HCompV error")
		print ("%s step. complete"%comp)

	#elif flow==4 :
		create.macros(vFloors,proto_new,hmm+'0')
		create.hmmdefs(monophones,proto_new,hmm+'0')
		for i in range(0,7) :
			p=os.system("/home/pi/htk/HTKTools/HERest -C %s -I %s -t 250.0 150.0 1000.0 -S %s -H %s/macros -H %s/hmmdefs -M %s %s"%(config1,phone0,train,hmm+'%d'%i,hmm+'%d'%i,hmm+'%d'%(i+1),monophones))
			time.sleep(1)
			print("%d comp"%(i+1))

		if (os.path.exists("%s/macros"%(hmm+'1'))) :
			print("**HERest Complete**")
			print("")
			comp += "4."
		else : create.error("Hmm7 HERest error")
		print ("%s step. complete"%comp)

	#elif flow==5 :
		copyfile(phone0, "%s/aligned.mlf"%created_path)
		p=os.system("/home/pi/htk/HTKTools/HLEd -n %s/triphones -l '*' -i %s/wintri.mlf %s/mktri.led %s/aligned.mlf"%(created_path,created_path,based_path,created_path))
		time.sleep(1)
		if (os.path.exists("%s/wintri.mlf"%created_path)) :
			print("**Triphones Complete**")
			print("")
			comp += "5."
		else : create.error("wintri.mlf error")
		print ("%s step. complete"%comp)

	#elif flow==6 :
		p=os.system("perl %s/maketrihed %s %s/triphones %s"%(based_path,monophones,created_path,created_path))
		time.sleep(1)
		if (os.path.exists("%s/mktri.hed"%created_path)) :
			print("**Make_mktri.hed Complete**")
			print("")
			comp += "6."
		else : create.error("mktri.hed error")
		print ("%s step. complete"%comp)

	#elif flow==7 :
		p=os.system("/home/pi/htk/HTKTools/HHEd -B -H %s/macros -H %s/hmmdefs -M %s %s/mktri.hed %s"%(hmm+'7',hmm+'7',hmm+'8',created_path,monophones))
		time.sleep(1)
		if (os.path.exists("%s/hmmdefs"%(hmm+'8'))) :
			print("**HHEd Complete**")
			print("")
			comp += "7."
		else : create.error("HHEd error")
		print ("%s step. complete"%comp)

	#elif flow==8 :
		for i in range(0,2) :
			p=os.system("/home/pi/htk/HTKTools/HERest -B -C %s -I %s/wintri.mlf -t 250.0 150.0 1000.0 -s %s/stats \
	-S %s -H %s/macros -H %s/hmmdefs -M %s %s"%(config1,created_path,created_path,train,hmm+'%d'%(i+8),hmm+'%d'%(i+8),hmm+'%d'%(i+9),triphones))
			print("%d comp"%(i+9))
			time.sleep(1)

		p=os.system("/home/pi/htk/HTKTools/HParse %s/gram %s/wdnet"%(based_path,created_path))
		time.sleep(0.5)
		if (os.path.exists("%s/wdnet"%created_path)) :
			print("**HERest Complete**")
			print("")
			comp += "8."
		else : create.error("HParse error")
		print ("%s step. complete"%comp)

	#elif flow==9 :
		os.system("perl %s/mkclscript.prl TB 350.0 %s > %s/tree.hed"%(based_path,monophones,created_path))
		create.tree(created_path)
		if (os.path.exists("%s/tree.hed"%created_path)) :
			print("**Perl Complete**")
			print("")
			comp += "9."
		else : create.error("tree.hed error")
		print ("%s step. complete"%comp)

	#elif flow==10 :
		os.system("/home/pi/htk/HTKTools/HHEd -B -H %s/macros -H %s/hmmdefs -M %s %s/tree.hed %s > %s/log"%((hmm+'10'),(hmm+'10'),(hmm+'11'),created_path,triphones,created_path))
		time.sleep(1)
		if (os.path.exists("%s/tiedlist"%created_path)) :
			print("**Tied Complete**")
			print("")
			comp += "10."
		else : create.error("Tiedlist error")
		print ("%s step. complete"%comp)

	#elif flow==11 :
		for i in range(0,2) :
			p=os.system("/home/pi/htk/HTKTools/HERest -B -C %s -I %s/wintri.mlf -t 250.0 150.0 1000.0 -s %s/stats \
	-S %s -H %s/macros -H %s/hmmdefs -M %s %s/tiedlist"%(config1,created_path,created_path,train,hmm+'%d'%(i+11),hmm+'%d'%(i+11),hmm+'%d'%(i+12),created_path))
			print("%d comp"%(i+12))
			time.sleep(1)

		if (os.path.exists("%s/macros"%(hmm+'13'))) :
			print("**HERest Complete**")
			print("")
			comp += "11."
		else : create.error("Hmm13 HERest error")
		print ("%s step. complete"%comp)

	#elif flow==12 :
		p=os.system("/home/pi/htk/HTKTools/HVite -C %s -H %s/macros -H %s/hmmdefs -S %s -l '*' -i %s/recout.mlf -w %s/wdnet -p 0.0 -s 5.0 %s %s/tiedlist"%(config2,hmm+'13',hmm+'13',train,created_path,created_path,diction,created_path))
		time.sleep(1)
		if (os.path.exists("%s/recout.mlf"%created_path)) :
			print("**HVite Complete**")
			print("")
			comp += "12."
		else : create.error("HVite error")
		print ("%s step. complete"%comp)

	#elif flow==13 :
		result=os.popen("/home/pi/htk/HTKTools/HResults -I %s/words.mlf %s/tiedlist %s/recout.mlf"%(created_path,created_path,created_path)).readlines()
		result=''.join(result)
		print result
	
		got = open('%s/Trainning_result'%created_path,'w')
		got.write(result)
		got.close()

		if (os.path.exists("%s/Trainning_result"%created_path)) :
			print("**HResults Complete**")
			print("")
		else : create.error("Result error")

		os.system("mv /home/pi/workspace2/trainning /home/pi/workspace2/trainning_%s"%time.strftime("_%m%d_%H%M"))

		copytree(created_path,final)
		print("***TRAINNING COMPLETE***")

	elif flow ==0 : 
		print ("** Have a nice day :) **")
		break
	else : print("**Command Repeat**")



