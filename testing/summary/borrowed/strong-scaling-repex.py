import os
import sys
import time
import math
import datetime
import numpy as np
import matplotlib.pyplot as plt
from textwrap import wrap

PWD    = os.path.dirname(os.path.abspath(__file__))

#------------------------------------------------------------------------------

def calc_standard_err(data):

    size = len(data)
    # standard deviation
    std = np.std(data)
    # error
    std_error = std / (math.sqrt(size))

    return std_error

#-------------------------------------------------------------------------------

def read_data(name, cycle, cores):

    try:
        r_file = open('../data/data.2.1/' + name + ".csv", "r")
    except IOError:
        print 'Warning: unable to access template file...'

    line_buffer = r_file.readlines()
    r_file.close()

    md_times = []
    md_times_err = []

    exchange_times = []
    exchange_times_err = []

    data_times = []
    data_times_err = []
    overhead_times = []
    
    md_times_new = []
    md_times_stagein = []
    md_times_alloc = []
    md_times_exec = []
    md_times_stageout = []
    md_times_done = []

    exchange_times_new = []
    exchange_times_stagein = []
    exchange_times_alloc = []
    exchange_times_exec = []
    exchange_times_stageout = []
    exchange_times_done = []


    for line in line_buffer:
        row = line.split(';')

        for i in range(len(row)):
            row[i] = row[i].lstrip()

        if (len(row) > 2):
            if row[0].startswith('unit') and row[8].startswith('md_step'):
                if row[7] == cycle:
                    md_times_new.append(float(row[1]))
                    md_times_stagein.append(float(row[2]))
                    md_times_alloc.append(float(row[3]))
                    md_times_exec.append(float(row[4]))
                    md_times_stageout.append(float(row[5]))
                    md_times_done.append(float(row[6]))
            
            # if ex
            if row[0].startswith('unit') and row[8].startswith('ex_step'):
                if row[7] == cycle:
                    exchange_times_new.append(float(row[1]))
                    exchange_times_stagein.append(float(row[2]))
                    exchange_times_alloc.append(float(row[3]))
                    exchange_times_exec.append(float(row[4]))
                    exchange_times_stageout.append(float(row[5]))
                    exchange_times_done.append(float(row[6]))

        # step timings
        if (len(row) > 2):
            if row[0].startswith(cycle) and row[1] == 'md_step':                
                md_step_start    = float(row[2])
                md_step_stop     = float(row[3])
                md_step_duration = float(row[4])

            if row[0].startswith(cycle) and row[1] == 'ex_step':
                ex_step_start    = float(row[2])
                ex_step_stop     = float(row[3])
                ex_step_duration = float(row[4])
            if row[0].startswith(cycle) and row[1] == 'pp_step':
                pp_step_start    = float(row[2])
                pp_step_stop     = float(row[3])
                pp_step_duration = float(row[4])

        # enmd overhead step timings
        if (len(row) > 2):
            if row[0].startswith(cycle) and row[1].startswith('md_step_enmd_overhead'):
                enmd_md_step_start    = float(row[2])
                enmd_md_step_stop     = float(row[3])
                enmd_md_step_duration = float(row[4])
            if row[0].startswith(cycle) and row[1].startswith('ex_step_enmd_overhead'):
                enmd_ex_step_start    = float(row[2])
                enmd_ex_step_stop     = float(row[3])
                enmd_ex_step_duration = float(row[4])
            if row[0].startswith(cycle) and row[1].startswith('pp_step_enmd_overhead'):
                enmd_pp_step_start    = float(row[2])
                enmd_pp_step_stop     = float(row[3])
                enmd_pp_step_duration = float(row[4])

    #---------------------------------------------------------------------------
    # exec

    temp = ( max(md_times_stageout) - min(md_times_exec) )
    md_times.append(temp)

    temp = ( max(exchange_times_stageout) - min(exchange_times_exec) )
    exchange_times.append( temp )

    #---------------------------------------------------------------------------
    # data
    
    md_data = []

    data_in = []
    data_out = []
    for i in range(len(md_times_new)):
        d_out = ( md_times_done[i]  - md_times_stageout[i] )
        d_in  = ( md_times_alloc[i] - md_times_stagein[i] )
        data_in.append(d_in)
        data_out.append(d_out)

    d_out = ( max(exchange_times_done)  - min(exchange_times_stageout) )
    d_in  = ( max(exchange_times_alloc) - min(exchange_times_stagein) )
    ex_data = (d_in + d_out)

    # hardcoded, since we have 640 replicas
    data_times.append( np.mean(data_in) + ( np.mean(data_out) * (640.0 / cores) ) + ex_data )

    #---------------------------------------------------------------------------

    tmp_md_exec = sorted(md_times_exec)
    rp_over1 = abs((tmp_md_exec[cores-1] - tmp_md_exec[0]))

    enmd_over1 = float(enmd_md_step_duration)

    #---------------------------------------------------------------------------

    temp2      = float(ex_step_duration)
    enmd_over2 = float(enmd_ex_step_duration)

    rp_over2 = np.mean(exchange_times_exec) - np.mean(exchange_times_alloc)
    rp_overhead = rp_over1 + rp_over2

    #---------------------------------------------------------------------------

    enmd_over3 = float(enmd_pp_step_duration)
    enmd_overhead   = enmd_over1 + enmd_over2 + enmd_over3

    return md_times[0], exchange_times[0], data_times[0], rp_overhead, enmd_overhead  
    
