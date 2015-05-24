import math
import os
from sys import argv

'''
File = open("yo.txt","w")

# vary the set size in powers of 2 from 2 to 1024
for i in xrange(4,17,4):
	# vary the core size in powers of 2 from 2 to 1024
	for j in range(1,5):
		# Gather four instances of data from an experiment
		for k in range(1,5):
			exec_line = "python allpairs_example.py {0} {1}\n".format(i,pow(4,j))
			File.write(exec_line)
			#os.system(exec_line)

File.close()

'''

script, sc, cc = argv

setCount = int(sc)
coreCount = int(cc)

for i in range(1,5):
	exec_line = "python New_allpairs.py {0} {1}\n".format(setCount,coreCount)
	os.system(exec_line)
	#print exec_line


