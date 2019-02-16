import os
import time

c_dic={}
dic={1:"Left", 2:"Right", 3:"Emergency", 4:"Go", 5:"Stop", 6:"Noise"}
current=[word.strip('\n') for word in os.popen("ls /home/pi").readlines() if word != "wav.py\n"]
max=max([len(word) for word in current])

while True:
	for i in current:
		c_dic[current.index(i)]=i
		command=dic.get(current.index(i))
		print current.index(i),":",
		while len(i) < max :
			i+=' '
		print i,
		print "  ->",command 
	print "8 : EXIT"

	path=c_dic.get(input("Select the path : "))
	
	if path==None :
		print("$$BYE$$")
		break
	cmd=dic.get(input("Enter the cmd : "))
	if cmd==None :
		print("$$BYE$$")
		break

	final="/home/pi/%s/%s"%(path,cmd)
	got=[word.strip('\n') for word in os.popen("ls %s"%final).readlines()]
	for i in got:
		if i[-5:] != '.mfcc' :
			os.system("aplay %s/%s"%(final,i))
			time.sleep(1)
