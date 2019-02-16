import sys
sys.path.append("/usr/lib/python2.7/test/test")

import perm
def get():
	q,w,e,r,t,y=perm.get()
	if y==0:
		raise ValueError

	return q,w,e,r,t,y
