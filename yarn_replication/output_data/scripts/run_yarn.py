import os
import sys
import math

k_list = [50,500,5000]
task_list = [8,16,32]
input_files = ["../data/dataset_1M_3d.in", "../data/dataset_100K_3d.in", "../data/dataset_10K_3d.in"]

name_map = {
	"dataset_1M_3d.in": "1M",
	"dataset_100K_3d.in": "100K",
	"dataset_10K_3d.in": "10K"
}

types = ["xsede.stampede","xsede.stampede_yarn"]

# test = open("files.txt","w")

for k in k_list:
	for task in task_list:
		for type_name in types:
			input_filename = input_files[int(math.ceil(math.log(k/5,10))) - 1]
			# "python k-means-ioannis.py k dim #tasks #cores <input file name> <report file name> <queue>"
			report_filename = "{0}_{1}_{2}.txt".format(k,task,type_name)
			os.system("python k-means.py {0} 3 {1} {1} {2} {3} development {4}".format(k,task,input_filename,report_filename,type_name))
			#test.write("python k-means.py {0} 3 {1} {1} {2} {3} development {4}\n".format(k,task,input_filename,report_filename,type_name))
# test.close()


