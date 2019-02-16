import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('X',type=int)
parser.add_argument('Y',type=int)

args = parser.parse_args()
fron = args.X
to = args.Y
print fron, to

for i in range(fron,to+1) :
	os.system("sudo rm data%d.mfcc"%i)
	print "Remove data%d.mfcc"%i

