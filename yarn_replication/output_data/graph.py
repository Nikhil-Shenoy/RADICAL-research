import matplotlib.pyplot as plt
import csv
import math
import numpy as np

data = {
	50: {
		8: {
			"stampede": 0,
			"stampede_yarn": 0
		},
		16: {
			"stampede": 0,
			"stampede_yarn": 0
		},
		32: {
			"stampede": 0,
			"stampede_yarn": 0
		},
	},
	500: {
		8: {
			"stampede": 0,
			"stampede_yarn": 0
		},
		16: {
			"stampede": 0,
			"stampede_yarn": 0
		},
		32: {
			"stampede": 0,
			"stampede_yarn": 0
		},
	},
	5000: {
		8: {
			"stampede": 0,
			"stampede_yarn": 0
		},
		16: {
			"stampede": 0,
			"stampede_yarn": 0
		},
		32: {
			"stampede": 0,
			"stampede_yarn": 0
		},
	}
}

errors = {
	50: {
		8: {
			"stampede": 0,
			"stampede_yarn": 0
		},
		16: {
			"stampede": 0,
			"stampede_yarn": 0
		},
		32: {
			"stampede": 0,
			"stampede_yarn": 0
		},
	},
	500: {
		8: {
			"stampede": 0,
			"stampede_yarn": 0
		},
		16: {
			"stampede": 0,
			"stampede_yarn": 0
		},
		32: {
			"stampede": 0,
			"stampede_yarn": 0
		},
	},
	5000: {
		8: {
			"stampede": 0,
			"stampede_yarn": 0
		},
		16: {
			"stampede": 0,
			"stampede_yarn": 0
		},
		32: {
			"stampede": 0,
			"stampede_yarn": 0
		},
	}
}

points = {
	50: 1000000,
	500: 100000,
	5000: 10000
}

clusters = [50,500,5000]
tasks = [8,16,32]
resource = ["stampede","stampede_yarn"]

for c in clusters:
	for t in tasks:
		for r in resource:
			f = "{0}/{0}_{1}_{2}.csv".format(c,t,r)
			# print("\n{0}\n".format(f))
			input_file = open(f,'r')
			reader = csv.reader(input_file)
			next(reader) # Skips the header

			exec_times = np.array([],dtype=float)
			for line in reader:
				if line[7] != "N/A" and line[3] != "N/A":
					exec_times = np.append(exec_times,float(line[7]) - float(line[3]))

			average = np.mean(exec_times)
			std_error = np.std(exec_times) / math.sqrt(np.size(exec_times))


			data[c][t][r] = average
			errors[c][t][r] = std_error

			# print("{0} ---> {1}".format(f,average))
			input_file.close()

# Collected all the data; Let's graph

N = 3
for c in clusters:
	stampede_data = np.array([],dtype=float)
	stampede_errors = np.array([],dtype=float)
	yarn_data = np.array([],dtype=float)
	yarn_errors = np.array([],dtype=float)

	for t in tasks:
		stampede_data = np.append(stampede_data,data[c][t]["stampede"])
		stampede_errors = np.append(stampede_errors,errors[c][t]["stampede"])
		yarn_data = np.append(yarn_data,data[c][t]["stampede_yarn"])
		yarn_errors = np.append(yarn_errors,errors[c][t]["stampede_yarn"])

	fig, ax = plt.subplots()

	ind = np.arange(N)
	width = .35

	# linestyle = {"linewidth":3,"markeredgewidth":4}
	linestyle = {}
	r1 = ax.bar(ind,stampede_data,width,color='lightskyblue')
	ax.errorbar(ind + width/2,stampede_data,yerr=stampede_errors,color='k',ls='none',**linestyle)
	r2 = ax.bar(ind + width,yarn_data,width,color='lawngreen')
	ax.errorbar(ind + width/2 + width,yarn_data,yerr=yarn_errors,color='k',ls='none',**linestyle)


	ax.set_ylabel("Execution Time (sec)")
	ax.set_title("K-means Experiment Using {0} Clusters and {1} Points".format(c,points[c]))
	ax.set_xticks(ind + width)
	ax.set_xticklabels(('8','16','32'))
	ax.set_xlabel("Tasks = Cores")

	ax.legend((r1[0],r2[0]),('RADICAL-Pilot',"RADICAL-Pilot-YARN"))

	plt.grid()
	plt.savefig("graphs/{0}.png".format(c))


