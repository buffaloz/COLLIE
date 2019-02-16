import os

def create_codetr(path):
	st_st=["/Left","/Right","/Emergency","/Go","/Stop","/Noise"]
	frame=[]
	for repeat in range(6):
		f=[word.split() for word in os.popen("ls %s%s"%(path,st_st[repeat])).readlines()]
		for i in f :
			frm=[]
			for j in i :
				j=path+st_st[repeat]+'/'+j
				frm.append(j)
			b=' '.join(frm)
			frame.append(b)
	fframe=[]
	for i in frame:
		i=i+' '+i[:-4]+'.mfcc\n'
		fframe.append(i)
	new=open("%s/created_prac/new.scp"%path,'w')
	new.write(b''.join(fframe))
	new.close()

if __name__ == '__main__':
	create_codetr(path)
