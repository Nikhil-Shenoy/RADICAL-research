import math
import os


for i in os.listdir(os.getcwd()):
	if i.endswith(".txt"):
		File = open(i,"r")
		line = File.readlines() # Now we have all the lines in the file
		File.close()
		data = []
		for j in range(0,len(line)):
			data.append(float(line[j]))
			
	
		average = sum(data) / len(data)

		print "The average for file %s is: %f\n" % (i,average)

		File = open(i,"w")
		File.write(str(average))
		File.write("\n")
		File.close()

		
			
		
