from radical.ensemblemd import Kernel
from radical.ensemblemd import Pipeline
from radical.ensemblemd import EnsemblemdError
from radical.ensemblemd import SingleClusterEnvironment
import os

class MyApp(Pipeline):
	def __init__(self, instances):
		Pipeline.__init__(self,instances)

	def step_1(self, instance):
		k = Kernel(name="misc.chksum")
		k.arguments = ["--inputfile=UTF-8-demo.txt", "--outputfile=checksum{0}.sha1".format(instance)]
	        k.download_input_data  = "http://testing.saga-project.org/cybertools/UTF-8-demo.txt"
       	 	k.download_output_data = "checksum{0}.sha1".format(instance)
	        return k

if __name__ == "__main__":

	os.system("clear")

	cluster = SingleClusterEnvironment(
		resource = "localhost",
		cores = 1,
		walltime = 15,
		username = None,
		allocation = None
	)

	app = MyApp(instances=1)
	cluster.run(app)





