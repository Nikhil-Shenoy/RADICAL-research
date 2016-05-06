import os


directories = ["50","500","5000"]
path = "/home/shenoy/Documents/Nikhil/research/RADICAL-research/yarn_replication/output_data/"
exe = "/home/shenoy/Documents/Nikhil/research/RADICAL-research/yarn_replication/midas/supporting_scripts/filter_yarn_output.py"

for d in directories:
	for f in os.listdir(path + d + "/"):
		current_file = path + d + "/" + f
		new_file = path + d + "/" + "mod_" + f

		os.system("python {0} {1} {2}".format(exe,current_file,new_file))
		os.system("mv {0} {1}".format(new_file,current_file))