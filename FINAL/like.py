def result():
	f=open("/home/pi/result/recout1.mlf",'r')
	con=f.readlines()
	word=(con[3].split())[2]
	print "\n\nRecording word : "+word + "\n"

	L_1=float((con[2].split())[3])+float((con[3].split())[3])+float((con[4].split())[3])
	L_2=float((con[6].split())[3])+float((con[7].split())[3])+float((con[8].split())[3])
	L_3=float((con[10].split())[3])+float((con[11].split())[3])+float((con[12].split())[3])
	L_4=float((con[14].split())[3])+float((con[15].split())[3])+float((con[16].split())[3])
	L_5=float((con[18].split())[3])+float((con[19].split())[3])+float((con[20].split())[3])
	L_6=float((con[22].split())[3])+float((con[23].split())[3])+float((con[24].split())[3])

	return word,L_1,L_2,L_3,L_4,L_5,L_6

if __name__ == "__main__" :
	result()
