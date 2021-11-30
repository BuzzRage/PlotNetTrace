#!/usr/bin/env python3

import numpy as np
import sys
import NetTrace
from matplotlib import pyplot as plt

def timefreq_plot(filename):
    
    rtr_measure = NetTrace.Measure(filename)
    rtr_measure.load_data()

    #Visualization part
    fig = plt.figure()
    r=4
    c=2

    plt.subplot(r, c, 1)
    plt.ylabel("Marking probability\n evolution (%)")
    plt.xlabel("time (in ms)")
    plt.plot(rtr_measure.x, rtr_measure.prob, color='blue')
    plt.grid()

    plt.subplot(r, c, 2)
    plt.ylabel("Marking probability\n occurrency")
    plt.hist(rtr_measure.prob, bins=np.arange(min(rtr_measure.prob),max(rtr_measure.prob)), density=False, color='blue')
    plt.grid()

    plt.subplot(r, c, 3)
    plt.ylabel("egress rate")
    plt.xlabel("time (in ms)")
    plt.plot(rtr_measure.x, rtr_measure.bytes_sent_t, color='green')
    plt.grid()

    plt.subplot(r, c, 4)
    plt.ylabel("egress rate\n value occurrency")
    interval = np.arange(min(rtr_measure.bytes_sent_t),max(rtr_measure.bytes_sent_t),400)
    plt.hist(rtr_measure.bytes_sent_t, bins=interval, density=False, color='blue')
    #plt.hist(rtr_measure.bytes_sent_t, bins=np.arange(min(rtr_measure.bytes_sent_t),max(rtr_measure.bytes_sent_t)), density=False, color='blue')
    plt.grid()

    plt.subplot(r, c, 5)
    plt.ylabel("lqueue delay (ms)")
    plt.plot(rtr_measure.x, rtr_measure.ldelay, '.', color='green')
    plt.yscale('log')
    plt.xlabel("time (in ms)")
    plt.grid()

    plt.subplot(r, c, 6)
    plt.ylabel("lqueue delay\n value occurrency")
    plt.hist(rtr_measure.ldelay, bins=np.arange(min(rtr_measure.ldelay),max(rtr_measure.ldelay)), density=False, color='blue')
    plt.grid
    
    plt.subplot(r, c, 7)
    plt.ylabel("Additional ECN marks\n value occurrency")
    interval2 = np.arange(min(rtr_measure.ecn_mark_t),max(rtr_measure.ecn_mark_t),100)
    plt.hist(rtr_measure.ecn_mark_t, bins=np.arange(min(rtr_measure.ldelay),max(rtr_measure.ldelay)), density=False, color='blue')
    plt.grid()
    
    plt.subplot(r, c, 8)
    plt.ylabel("Additional packet drop\n value occurrency")
    interval3 = np.arange(min(rtr_measure.pkt_dropped_t),max(rtr_measure.pkt_dropped_t),1)
    plt.hist(rtr_measure.pkt_dropped_t, bins=interval3, density=False, color='blue')
    #plt.plot(rtr_measure.x, rtr_measure.pkt_dropped, '.', color='red')
    plt.grid()

    plt.suptitle(filename)
    
    plt.show()

    
args   = list(sys.argv)

if(len(args) > 1):
    filename = args[1]
else:
    filename = "data/0840-rtr.raw"

timefreq_plot(filename)
