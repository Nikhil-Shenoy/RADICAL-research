import os
import sys
import time
import math
import datetime
import numpy as np
import matplotlib.pyplot as plt
from textwrap import wrap

PWD    = os.path.dirname(os.path.abspath(__file__))

#-------------------------------------------------------------------------------

def calc_standard_err(data):

    size = len(data)
    # standard deviation
    std = np.std(data)
    # error
    std_error = std / (math.sqrt(size))

    return std_error

#-------------------------------------------------------------------------------

def minimize_data(data, minval):
    for i in range(len(data)):
        data[i] = data[i] - minval
    return data

#-------------------------------------------------------------------------------

def read_data(name, cycle):

    try:
        r_file = open('../data/' + name + ".csv", "r")
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


        #print row

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

        #-----------------------------------------------------------------------
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
    #---------------------------------------------------------------------------
    #---------------------------------------------------------------------------
    # exec

    md_list = []
    for i in range(len(md_times_new)):
        md_temp = (md_times_stageout[i] - md_times_exec[i]).total_seconds()
        md_list.append(md_temp)

    md_times.append(np.mean(md_list))

    temp = calc_standard_err(md_list)
    md_times_err.append(temp)

    ex_list = []
    for i in range(len(exchange_times_new)):
        ex_temp = (exchange_times_stageout[i] - exchange_times_exec[i]).total_seconds()
        ex_list.append(ex_temp)

    exchange_times.append(np.mean(ex_list))

    temp = calc_standard_err(ex_list)
    exchange_times_err.append(temp)


    #---------------------------------------------------------------------------
    # data

    md_data = []
    for i in range(len(md_times_new)):
        d_out = abs( (md_times_done[i]  - md_times_stageout[i]).total_seconds() )
        d_in  = abs( (md_times_alloc[i] - md_times_stagein[i]).total_seconds() )
        md_data.append(d_in + d_out)

    ex_data = 0.0
    for i in range(len(exchange_times_new)):
        d_out = abs( (exchange_times_done[i]  - exchange_times_stageout[i]).total_seconds() )
        d_in  = abs( (exchange_times_alloc[i] - exchange_times_stagein[i]).total_seconds() )
        ex_data += (d_in + d_out)

    data_times.append(np.mean(md_data) + ex_data)

    temp_list = md_data
    temp_list.append(ex_data)

    temp = calc_standard_err(temp_list)
    data_times_err.append(temp)

    #---------------------------------------------------------------------------
    # overhead
   
    temp1      = float(md_step_duration)
    enmd_over1 = float(enmd_md_step_duration)

    # rp overhead for md step
    rp_over1 = temp1 - md_times[0] - np.mean(md_data) - enmd_over1

    #---------------------------------------------------------------------------
    temp2      = float(ex_step_duration)
    enmd_over2 = float(enmd_ex_step_duration)

    rp_over2 = temp2 - exchange_times[0] - np.mean(ex_data) - enmd_over2

    enmd_over3 = float(enmd_pp_step_duration)

    rp_overhead = rp_over1 + rp_over2

    enmd_overhead   = enmd_over1 + enmd_over2 + enmd_over3

    return md_times[0], exchange_times[0], data_times[0], rp_overhead, enmd_overhead  
    
