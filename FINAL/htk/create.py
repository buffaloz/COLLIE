#-*- coding: utf-8 -*-
import os.path

#Inspire an error
def error(flow) :
	print ("!! %s: Error!!"%flow)

#Edit tree.hed
def tree(path) :

	got = [word for word in open('%s/tree.hed'%path,'r').readlines()]
	gotit = ['LS "%s/stats"\n'%path] + got + ['CO "%s/tiedlist"'%path]
	gotit=''.join(gotit)

	got = open(path+'/tree.hed','w')
	got.write(gotit)
	got.close

#Create hmmdefs in hmm0
def hmmdefs(monophones,proto,hmm0) :

	got = open(hmm0+'/hmmdefs','w')
	gotit = [word for word in open(proto,'r').readlines()]
	gotit1 = [word.strip('\r\n') for word in open(monophones,'r').readlines()]
	got.write(gotit[0])
	got.write(gotit[1])
	got.write(gotit[2])
	gotit=gotit[3:]

	for j in gotit1 :	
		for i in gotit :
			if 'proto' in i :
				i='~h "%s"\n'%j

			got.write(i)

	print("**hmmdefs EDITED**\n"),
	got.close

#Create macros in hmm0
def macros(vFloors,proto,hmm0) :
	gotit = [word for word in open(proto,'r').readlines()]
	gotit1 = [word for word in open(vFloors,'r').readlines()]

	got = open(hmm0+'/macros','w')
	got.write(gotit[0])
	got.write(gotit[1])
	got.write(gotit[2])

	for i in gotit1 :
		got.write(i)
	
	print("**macros EDITED**\n"),
	got.close()

#Make directory(trainning_path) with no overlap
def directory(trainning_path) :
	i=0
	
	while (os.path.exists(trainning_path)) :
		i+=1
		if 'g' in trainning_path[(len(trainning_path)-1):] :
			trainning_path="%s%d"%(trainning_path,i)

		elif (len(trainning_path)==24):
			if (int(trainning_path[(len(trainning_path)-2):]) > 9) :
				trainning_path=trainning_path[:-2]
				trainning_path="%s%d"%(trainning_path,i)
		else :
			trainning_path=trainning_path[:-1]
			trainning_path="%s%d"%(trainning_path,i)

		print ("#. %d"%i)
	return trainning_path

#Create monophones Using By diction.txt
def monophones(diction,path) :

	data = [word.strip('\n').split(' ') for word in open(diction, 'r').readlines()]
	datt=[]
	for i in range(0,6) :
		dat=data[i]
		dat = [x for x in dat if ((x != "n\r")&(x != "iy\r")&(x != "uh\r")&(x != "LEFT")&(x != "RIGHT")&(x != "EMERGENCY")&(x != "STOP")&(x != "GO")&(x != "sil\r")&(x != "NOISE")&(x != ""))]#.decode('utf-8')
		datt+=dat
	
	dattt=set(datt)
	gotit=open(path+'/monophones','w')#.readline()#.decode('utf-8')

	for i in dattt :
		gotit.write(i+'\n')

	print("**monophones EDITED**\n"),
	gotit.close()


#Create HMM folders
def mkdir_hmm(path):

	for i in range(0,14) :
		p=os.system("mkdir %s/hmm%d"%(path,i))
		print("**HMM%d folders made**\n"%i),


#Create codetr.scp
def codetr(codetr,code) :

	gotit=open(codetr,'w')#.readline()#.decode('utf-8')

	for i in code :
		i=i[:len(i)-4]
		gotit.write('%s.wav %s.mfcc\n'%(i,i))

	print("**codetr.scp EDITED**\n"),
	gotit.close()

#Create train.scp
def train(train,code) :

	gotit=open(train,'w')#.readline()#.decode('utf-8')

	for i in code :
		i=i[:len(i)-4]
		gotit.write('%s.mfcc\n'%i)
	got=open("/home/pi/based_files/previousDB/train.scp",'r').readlines()
	got=''.join(got)
	gotit.write(got)
	print("**train.scp EDITED**\n"),
	gotit.close()

#Create word0.mlf
def words(words,code,trainning_path) :

	cmd1_path="%s/Left"%trainning_path
	cmd2_path="%s/Right"%trainning_path
	cmd3_path="%s/Emergency"%trainning_path
	cmd4_path="%s/Go"%trainning_path
	cmd5_path="%s/Stop"%trainning_path
	cmd6_path="%s/Noise"%trainning_path

	gotit=open(words,'w')#.readline()#.decode('utf-8')
	gotit.write("#!MLF!#\n")

	for i in code :

		if "Left" in i :
			gotit.write('"*')
			i=i[len(cmd1_path):len(i)-4]
			gotit.write(i)
			gotit.write('.lab"\n')
			gotit.write("LEFT\n")#.decode('utf-8')
			gotit.write('.\n')

		elif "Right" in i :
			gotit.write('"*')
			i=i[len(cmd2_path):len(i)-4]
			gotit.write(i)
			gotit.write('.lab"\n')
			gotit.write("RIGHT\n")#.decode('utf-8')
			gotit.write('.\n')	

		elif "Emergency" in i :
			gotit.write('"*')
			i=i[len(cmd3_path):len(i)-4]
			gotit.write(i)
			gotit.write('.lab"\n')
			gotit.write("EMERGENCY\n")#.decode('utf-8')
			gotit.write('.\n')

		elif "Go" in i :
			gotit.write('"*')
			i=i[len(cmd4_path):len(i)-4]
			gotit.write(i)
			gotit.write('.lab"\n')
			gotit.write("GO\n")#.decode('utf-8')
			gotit.write('.\n')

		elif "Stop" in i :
			gotit.write('"*')
			i=i[len(cmd5_path):len(i)-4]
			gotit.write(i)
			gotit.write('.lab"\n')
			gotit.write("STOP\n")#.decode('utf-8')
			gotit.write('.\n')
	
		elif "Noise" in i :
			gotit.write('"*')
			i=i[len(cmd6_path):len(i)-4]
			gotit.write(i)
			gotit.write('.lab"\n')
			gotit.write("NOISE\n")#.decode('utf-8')
			gotit.write('.\n')

	got=open("/home/pi/based_files/previousDB/words.mlf",'r').readlines()
	got=''.join(got)
	gotit.write(got)
	print("**words.mlf EDITED**\n"),
	gotit.close()
