from radical.ensemblemd import Pipeline
from radical.ensemblemd import Kernel
from radical.ensemblemd import EnsemblemdError
from radical.ensemblemd import SingleClusterEnvironment

class CalculateChecksums(Pipeline):

	def __init__(self, instances):
		Pipeline.__init__(self, instances)

	def step_1(self, instance):
		k = Kernel(name="misc.chksum")
		k.arguments = ["--inputfile=UTF-8-demo.txt", "--outputfile=checksum{0}.sha1".format(instance)]
		k.download_input_data = "http://testing.saga-project.org/cybertools/UTF-8-demo.txt"
		k.download_output_data = "checksum{0}.sha1".format(instance)

if __name__ == "__main__":

	try:
		cluster = SingleClusterEnvironment(
			resource="stampede.tacc.utexas.edu",
			cores = 12,
			walltime = 15,
			username="tg826231",
			allocation="TG-CCR140028"
		)

		cluster.allocate()
	
		ccount = CalculateChecksums(instances=16)

		cluster.run(ccount)

		print "\nResulting checksums:"
		import glob
		for result in glob.glob("checksum*.sha1"):
			print "  * {0}".format(open(result,"r").readline().strip())	


		import pprint
		pp = pprint.PrettyPrinter()
		pp.pprint(ccount.execution_profile_dict)

		df = ccount.execution_profile_dataframe
		df.to_pickle('results.pkl')

		df = pandas.read_pickle('result.pkl')
		print df

	
	except EnsemblemdError, er:
		print "EnsembleMD Error: {0}".format(str(er))
		raise
