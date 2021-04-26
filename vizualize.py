#!/bin/python
import sys
import numpy as np
from matplotlib import pyplot as plt

if len(sys.argv) > 0:
    finput = str(sys.argv[1])
else:
    finput = 'input.data'


def raw_to_csv():
    with open('data.csv', 'w') as csv_file, open(finput, 'r') as raw_file:
        for line in raw_file:
            csv_file.write(line.replace(" ", ""))

def plot_csv():
    csv = np.genfromtxt('data.csv', delimiter=",", skip_header=1)

    # Loading part
    x       = np.arange(0,len(csv))
    cwnd_CC = csv[:,0]
    MSS_CC  = csv[:,1]
    cwnd_C  = np.multiply(cwnd_CC, MSS_CC)
    cwnd_LC = csv[:,2]
    MSS_LC  = csv[:,3]
    cwnd_CS = csv[:,4]
    MSS_CS  = csv[:,5]
    cwnd_LS = csv[:,6]
    MSS_LS  = csv[:,7]
    droprate= csv[:,8]
    markrate= csv[:,9]
    qlen_C  = csv[:,11]
    qlen_L  = csv[:,10]

    # Statistics part
    cwnd_CC_mean = sum(cwnd_CC)/len(cwnd_CC)
    MSS_CC_mean  = sum(MSS_CC)/len(MSS_CC)
    cwnd_C_mean  = sum(cwnd_C)/len(cwnd_C)
    cwnd_LC_mean = sum(cwnd_LC)/len(cwnd_LC)
    MSS_LC_mean  = sum(MSS_LC)/len(MSS_LC)
    cwnd_CS_mean = sum(cwnd_CS)/len(cwnd_CS)
    MSS_CS_mean  = sum(MSS_CS)/len(MSS_CS)
    cwnd_LS_mean = sum(cwnd_LS)/len(cwnd_LS)
    MSS_LS_mean  = sum(MSS_LS)/len(MSS_LS)
    droprate_mean= sum(droprate)/len(droprate)
    markrate_mean= sum(markrate)/len(markrate)
    qlen_C_mean  = sum(qlen_C)/len(qlen_C)
    qlen_L_mean  = sum(qlen_L)/len(qlen_L)
    
    #Visualization part
    r=4
    c=2
    plt.subplot(r, c, 1)
    plt.xlabel("time (in RTT)")
    plt.ylabel("cwnd CC mean: "+"{:.2f}".format(cwnd_CC_mean))
    plt.plot(x, cwnd_CC)

    plt.subplot(r, c, 2)
    plt.xlabel("time (in RTT)")
    plt.ylabel("cwnd LC mean: "+"{:.2f}".format(cwnd_LC_mean))
    plt.plot(x, cwnd_LC)

    plt.subplot(r, c, 3)
    plt.xlabel("time (in RTT)")
    plt.ylabel("cwnd CS mean: "+"{:.2f}".format(cwnd_CS_mean))
    plt.plot(x, cwnd_CS)

    plt.subplot(r, c, 4)
    plt.xlabel("time (in RTT)")
    plt.ylabel("cwnd LS mean: "+"{:.2f}".format(cwnd_LS_mean))
    plt.plot(x, cwnd_LS)

    plt.subplot(r, c, 5)
    plt.xlabel("time (in RTT)")
    plt.ylabel("drop rate mean: "+"{:.2f}".format(droprate_mean))
    plt.plot(x, droprate)

    plt.subplot(r, c, 6)
    plt.xlabel("time (in RTT)")
    plt.ylabel("mark rate mean: "+"{:.2f}".format(markrate_mean))
    plt.plot(x, markrate)

    plt.subplot(r, c, 7)
    plt.xlabel("time (in RTT)")
    plt.ylabel("qlen_C mean: "+"{:.2f}".format(qlen_C_mean))
    plt.plot(x, qlen_C)

    plt.subplot(r, c, 8)
    plt.xlabel("time (in RTT)")
    plt.ylabel("qlen_L mean: "+"{:.2f}".format(qlen_L_mean))
    plt.plot(x, qlen_L)

    plt.suptitle("Visualisation des résultats")
    plt.show()




raw_to_csv()
plot_csv()
