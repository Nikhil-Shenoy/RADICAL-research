#!/usr/bin/env python

__author__       = "Ole Weider <ole.weidner@rutgers.edu>"
__copyright__    = "Copyright 2014, http://radical.rutgers.edu"
__license__      = "MIT"
__example_name__ = "Pipeline Example (generic)"


from radical.ensemblemd import Kernel
from radical.ensemblemd import Pipeline
from radical.ensemblemd import EnsemblemdError
from radical.ensemblemd import SingleClusterEnvironment
from random import shuffle

import pickle
import datetime
import pprint
import random
import sys
import os
import numpy as np


# ------------------------------------------------------------------------------
#
class CharCount(Pipeline):
    def __init__(self, instances, steps):
        Pipeline.__init__(self, instances, steps)

    def stage_1(self, instance):
        k = Kernel(name="misc.mkfile")
        k.arguments = ["--size=10000000", "--filename=asciifile-{0}.dat".format(instance)]
        return k

    def stage_2(self, instance):
        k = Kernel(name="misc.ccount")
        k.arguments            = ["--inputfile=asciifile-{0}.dat".format(instance), "--outputfile=cfreqs-{0}.dat".format(instance)]
        k.link_input_data      = "$STEP_1/asciifile-{0}.dat".format(instance)
        k.download_output_data = "cfreqs-{0}.dat".format(instance)
        k.cores = 1
        return k


def find_profile(files):
    for item in files:
        index = item.find('execution_profile')
        if index != -1:
            return item

def cleanup():
    os.system('rm *.dat')
# ------------------------------------------------------------------------------
#
if __name__ == "__main__":

    try:
        # Create a new static execution context with one resource and a fixed
        # number of cores and runtime.

        pp = pprint.PrettyPrinter()
    	#scale = [1,16,32,64,128]
        
        scale = [1,16,32,64,128]
        num_of_iterations = 4 
    	pairings = []

        for core in scale:
            for i in range(0,num_of_iterations):
                pairings.append((core,i))

        done = [(1,0),(128,2),(128,3),(32,0),(32,1),(32,2)]
        for item in done:
            pairings.remove(item)
    	pp.pprint(pairings)

    	shuffle(pairings)

    	for item in pairings:
            core_count = item[0]
            iteration = item[1] 
        
            cluster = SingleClusterEnvironment(
                resource="xsede.stampede",
                # resource="xsede.comet",
                # resource = "localhost",
                cores=core_count,
                walltime=30,
                username="tg826231",
                # username="nrs76",
                project="TG-MCB090174",
                database_url=os.environ.get('RADICAL_PILOT_DBURL'),
                database_name = 'enmddb',
                queue = "development"
            )

            # Allocate the resources. 
            cluster.allocate()
            ccount = CharCount(instances=core_count,steps=2)
            cluster.run(ccount)
            cluster.deallocate()

            new_core_string = "enmd_core_overhead_{0}_{1}.csv".format(core_count,iteration)
            new_core_string = "enmd_pat_overhead_{0}_{1}.csv".format(core_count,iteration)
            new_profile = "profile_{0}_{1}.csv".format(core_count,iteration)

            original_core = "enmd_core_overhead.csv"
            original_pattern = "enmd_pat_overhead.csv"
            original_profile = find_profile(os.listdir('.'))


            os.system("mv {0} {1}".format(original_core,new_core_string))
            os.system("mv {0} {1}".format(original_pattern,new_core_string))
            os.system("mv {0} {1}".format(original_profile, new_profile))


            cleanup()

            


    except EnsemblemdError, er:

        print "Ensemble MD Toolkit Error: {0}".format(str(er))
        raise # Just raise the execption again to get the backtrace
