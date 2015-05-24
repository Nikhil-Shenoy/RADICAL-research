import os
import numpy

def collect(path):
	f = open(path,'r')

	data = []
	data = f.readlines()
	print data	
	f.close()


for root, dires, files in os.walk('/home/nikhil/Documents/research/testing/experiments/allpairs/data/comp'):
	for name in files:
		if 'set-12' in name:
			collect(os.path.join(root,name))
