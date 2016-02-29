#!/usr/bin/env python


__author__       = "Ole Weider <ole.weidner@rutgers.edu>"
__copyright__    = "Copyright 2014, http://radical.rutgers.edu"
__license__      = "MIT"
__example_name__ = "Simulation-Analysis Example (generic)"

import math
import pandas
import pickle
import pprint
import datetime
import random
import os
import smtplib
import numpy as np

from radical.ensemblemd import Kernel
from radical.ensemblemd import SimulationAnalysisLoop
from radical.ensemblemd import EnsemblemdError
from radical.ensemblemd import SimulationAnalysisLoop
from radical.ensemblemd import SingleClusterEnvironment


# ------------------------------------------------------------------------------
#
class RandomSA(SimulationAnalysisLoop):
    def __init__(self, maxiterations, simulation_instances=1, analysis_instances=1):
        SimulationAnalysisLoop.__init__(self, maxiterations, simulation_instances, analysis_instances)

    def pre_loop(self):
            pass
    def simulation_step(self, iteration, instance):
        k = Kernel(name="misc.mkfile")
        k.arguments = ["--size=10000000", "--filename=asciifile.dat"]
        return k

    def analysis_step(self, iteration, instance):

        link_input_data = []
        for i in range(1,self.simulation_instances+1):
            link_input_data.append("$PREV_SIMULATION_INSTANCE_{instance}/asciifile.dat > asciifile-{instance}.dat".format(instance=i))

        k = Kernel(name="misc.ccount")
        k.arguments = ["--inputfile=asciifile.dat", "--outputfile=cfreqs.dat"]
        k.link_input_data = link_input_data
        k.download_output_data = "cfreqs.dat"
        k.cores = 1
        return k
	
    def post_loop(self):
        # post_loop is executed after the main simulation-analysis loop has
        # finished. In this example we don't do anything here.
        pass

def find_profile(files):
    for item in files:
        if item.find('execution_profile') != -1:
            return item

def cleanup():
    os.system('rm *.dat')
        

# ------------------------------------------------------------------------------
#
if __name__ == "__main__":

    try:
        # Create a new static execution context with one resource and a fixed
        # number of cores and runtime.

            scale = [1,16,32,64,128]
            num_of_iterations = 4
            #scale = [1]
            #num_of_iterations = 1
            pairings = []

            for core in scale:
                for i in range(0,num_of_iterations):
                    pairings.append((core,i))

            random.shuffle(pairings)

            pp = pprint.PrettyPrinter()
            pp.pprint(pairings)

            for item in pairings:
                core_count = item[0]
                iteration = item[1]
                # core_count = 1
                # iteration = 24
                instance_count = core_count
                cluster = SingleClusterEnvironment(
                    resource="xsede.stampede",
                    cores=core_count,
                    walltime=30,
                    username="tg826231",
                    project="TG-MCB090174",
                    database_url=os.environ.get('RADICAL_PILOT_DBURL'),
                    database_name = 'enmddb',
                    queue = "development"
                )

                cluster.allocate()
                randomsa = RandomSA(maxiterations=1, simulation_instances=instance_count, analysis_instances=instance_count)
                cluster.run(randomsa)
                cluster.deallocate()

                new_core = "enmd_core_overhead_{0}_{1}.csv".format(core_count,iteration)
                new_pattern = "enmd_pat_overhead_{0}_{1}.csv".format(core_count,iteration)
                new_profile = "profile_{0}_{1}.csv".format(core_count,iteration)

                original_core = "enmd_core_overhead.csv"
                original_pattern = "enmd_pat_overhead.csv"
                original_profile = find_profile(os.listdir('.'))

                os.system("mv {0} {1}".format(original_core,new_core))
                os.system("mv {0} {1}".format(original_pattern,new_pattern))
                os.system("mv {0} {1}".format(original_profile,new_profile))

                # cleanup()


    except EnsemblemdError, er:

        print "Ensemble MD Toolkit Error: {0}".format(str(er))
        raise # Just raise the execption again to get the backtrace
