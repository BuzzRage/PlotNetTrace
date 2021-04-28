#!/bin/python
import sys
import numpy as np
from parse import *
from matplotlib import pyplot as plt

ipath          = 'data/'
opath          = 'output/'
decode_from_ss = False

if len(sys.argv) > 0:
    finput = str(sys.argv[1])
    if len(sys.argv) > 2 and str(sys.argv[2]) == "ss":
        decode_from_ss = True
        cca = 0
else:
    finput = ipath+'data.raw'


class Measure:
    def __init__(self):
        self.x           = list()
        self.cwnd        = list()
        self.mss         = list()
        self.rtt         = list()
        self.bytes_acked = list()
        self.pacing_rate = list()
        
    def cwnd_mean(self):
        return sum(self.cwnd)/len(self.cwnd)
    
    def mss_mean(self):
        return sum(self.mss)/len(self.mss)
    
    def rtt_mean(self):
        return sum(self.rtt)/len(self.rtt)   
    
    def bytes_acked_mean(self):
        return sum(self.bytes_acked)/len(self.bytes_acked)
    
    def pacing_rate_mean(self):
        return sum(self.pacing_rate)/len(self.pacing_rate)    
    
    def load_from_csv(self,input_csv = opath+'data.csv'):        
        # Loading part. 
        # See https://www.man7.org/linux/man-pages/man8/ss.8.html for details
        # See /usr/include/linux/tcp.h for further details
        csv_cca            = 0  # Constant
        csv_wscale1        = 1  # <snd_wscale>
        csv_wscale2        = 2  # <rcv_wscale>
        csv_rto            = 3
        csv_rtt            = 4  # average RTT (ms)
        csv_rttvar         = 5  # mean deviation of RTT (RTTVAR) (ms)
        csv_mss            = 6
        csv_pmtu           = 7  # path MTU value
        csv_rcvmss         = 8
        csv_advmss         = 9  # Advertised MSS
        csv_cwnd           = 10
        csv_ssthresh       = 11
        csv_bytes_sent     = 12
        csv_bytes_acked    = 13
        csv_segs_out       = 14
        csv_segs_in        = 15
        csv_data_segs_out  = 16
        csv_send           = 17 # egress bps
        csv_lastsnd        = 18 # time (ms) since the last packet sent
        csv_lastrcv        = 19 # time (ms) since the last packet received
        csv_pacing_rate    = 20 
        csv_delivery_rate  = 21
        csv_delivered      = 22
        csv_busy           = 23
        #csv_unacked        =  # not parsed
        csv_rcv_space      = 24
        csv_rcv_thresh     = 25
        csv_notsent        = 26
        csv_minrtt         = 27
        
        csv = np.genfromtxt(input_csv, delimiter=",", skip_header=1)
        self.x           = np.arange(0,len(csv))
        self.cwnd        = csv[:,csv_cwnd]
        self.mss         = csv[:,csv_mss]
        self.rtt         = csv[:,csv_rtt]
        self.bytes_acked = csv[:,csv_bytes_acked]
        self.pacing_rate = csv[:,csv_pacing_rate]
        
def add_matched_field(field,line):
    return "NaN," if not search(field,line) else search(field,line)[0]+","

def decode_ss_line(line):
    decoded_line  = ""
    decoded_line += line.split()[cca]+","
    decoded_line += add_matched_field('wscale:{} ',line)  # generate two fields !
    decoded_line += add_matched_field('rto:{} ',line)
    rtt_temp = add_matched_field('rtt:{} ',line)
    decoded_line += rtt_temp.split("/")[0] + "," + rtt_temp.split("/")[1] if not rtt_temp == "NaN" else "NaN"
    decoded_line += add_matched_field('mss:{} ',line)
    decoded_line += add_matched_field('pmtu:{} ',line)
    decoded_line += add_matched_field('rcvmss:{} ',line)
    decoded_line += add_matched_field('advmss:{} ',line)
    decoded_line += add_matched_field('cwnd:{} ',line)
    decoded_line += add_matched_field('ssthresh:{} ',line)
    decoded_line += add_matched_field('bytes_sent:{} ',line)
    decoded_line += add_matched_field('bytes_acked:{} ',line)
    decoded_line += add_matched_field('segs_out:{} ',line)
    decoded_line += add_matched_field('segs_in:{} ',line)
    decoded_line += add_matched_field('data_segs_out:{} ',line)
    decoded_line += add_matched_field('send {}Gbps ',line)
    decoded_line += add_matched_field('lastsnd:{} ',line)
    decoded_line += add_matched_field('lastrcv:{} ',line)
    decoded_line += add_matched_field('pacing_rate {}Gbps ',line)
    decoded_line += add_matched_field('delivery_rate {}Gbps ',line)
    decoded_line += add_matched_field('delivered:{} ',line)
    decoded_line += add_matched_field('busy:{}ms ',line)
    decoded_line += add_matched_field('rcv_space:{} ',line)
    decoded_line += add_matched_field('rcv_ssthresh:{} ',line)
    decoded_line += add_matched_field('notsend:{} ',line) 
    decoded_line += add_matched_field('minrtt:{}',line)
    
    return str(decoded_line)+"\n"

def raw_to_csv():
    with open(opath+'data.csv', 'w') as csv_file, open(finput, 'r') as raw_file:
        raw_file.readline()
        for line in raw_file:
            if decode_from_ss:
                csv_file.write(decode_ss_line(line))
                #csv_file.write(line.split()[cwnd].split(":")[1]+","+line.split()[mss].split(":")[1]+",\n")
            else:
                csv_file.write(line.replace(" ", ""))

def plot_ss():
    
    measure1 = Measure()
    measure1.load_from_csv()
   
    #Visualization part
    r=2
    c=2
    plt.subplot(r, c, 1)
    plt.xlabel("time (in RTT)")
    plt.ylabel("cwnd mean: "+"{:.2f}".format(measure1.cwnd_mean()))
    plt.plot(measure1.x, measure1.cwnd)
    
    plt.subplot(r, c, 2)
    plt.xlabel("time (in RTT)")
    plt.ylabel("Average RTT mean: "+"{:.2f}".format(measure1.rtt_mean()))
    plt.plot(measure1.x, measure1.rtt)
    
    plt.subplot(r, c, 3)
    plt.xlabel("time (in RTT)")
    plt.ylabel("ACKed bytes mean: "+"{:.2f}".format(measure1.bytes_acked_mean()))
    plt.plot(measure1.x, measure1.bytes_acked)
    
    plt.subplot(r, c, 4)
    plt.xlabel("time (in RTT)")
    plt.ylabel("Pacing rate mean: "+"{:.2f}".format(measure1.pacing_rate_mean()))
    plt.plot(measure1.x, measure1.pacing_rate)    
    
    plt.suptitle("Visualisation des résultats")
    plt.show()
    
    
def plot_csv():
    csv = np.genfromtxt(opath+'data.csv', delimiter=",", skip_header=1)

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


#line = "cubic wscale:7,7 rto:204 rtt:0.43/0.179 mss:1460 pmtu:1500 rcvmss:536 advmss:1460 cwnd:1405 ssthresh:80 bytes_sent:27010249109 bytes_acked:27010249110 segs_out:18546357 segs_in:537945 data_segs_out:18546355 send 38.2Gbps lastsnd:4 lastrcv:56664 pacing_rate 20.3Gbps delivery_rate 1.72Gbps delivered:18546356 busy:55032ms rcv_space:14600 rcv_ssthresh:64076 minrtt:0.028"
#decode_ss_line(line)
raw_to_csv()

if decode_from_ss:
    plot_ss()
else:
    plot_csv()
