#!/bin/python
import sys
import getopt
import numpy as np
from pathlib import Path
from parse import *
from matplotlib import pyplot as plt

ipath          = 'data/'
opath          = 'output/'
decode_from_ss = True

args = sys.argv

if len(args) < 6:
    sys.exit("Invalid arguments. Expected usage:\n"+str(args[0])+" rtr_file atk_file cc_file lc_file cs_file ls_file\n")
else:
    if len(sys.argv) > 6 and str(sys.argv[2]) == "csv":
        decode_from_ss = False
    
    for arg in args[1:]:
        file_exist = Path(arg).is_file()
        if file_exist is not True:
            sys.exit(f"File {arg} does not exists")

    files = {}
    files["rtr_file"] = args[1]
    files["atk_file"] = args[2]
    files["cc_file"]  = args[3]
    files["lc_file"]  = args[4]
    files["cs_file"]  = args[5]
    files["ls_file"]  = args[6]

class Measure:
    def __init__(self, data_file = None):
        self.x             = list()
        self.cwnd          = list()
        self.mss           = list()
        self.rtt           = list()
        self.bytes_acked   = list()
        self.pacing_rate   = list()
        self.delivery_rate = list()
        self.delivered     = list()
        self.filename      = data_file
        
    def load_data(self):
        self.convert_raw_to_csv()
        if not self.is_router_data():
            self.load_from_csv()
        
    def is_router_data(self):
        with open(self.filename, 'r') as f:
            for line in f:
                if "dualpi2" in line:
                    return True
                elif "cubic" in line or "prague" in line:
                    return False
            
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
    
    def load_from_csv(self):        
        # Loading part. 
        # See https://www.man7.org/linux/man-pages/man8/ss.8.html for details
        # See `struct tcp_info` in /usr/include/linux/tcp.h for further details
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
        csv_busy           = 23 # Time (µs) busy sending data
        #csv_unacked        =  # not parsed
        csv_rcv_space      = 24
        csv_rcv_thresh     = 25
        csv_notsent        = 26
        csv_minrtt         = 27
        
        csv = np.genfromtxt(self.filename+".csv", delimiter=",", skip_header=1)
        self.x             = np.arange(0,len(csv))
        self.cwnd          = csv[:,csv_cwnd]
        self.mss           = csv[:,csv_mss]
        self.rtt           = csv[:,csv_rtt]
        self.bytes_acked   = csv[:,csv_bytes_acked]
        self.pacing_rate   = csv[:,csv_pacing_rate]
        self.delivery_rate = csv[:,csv_delivery_rate]
        self.delivered     = csv[:,csv_delivered]

    def add_matched_field(self,field,line):
        return "NaN," if not search(field,line) else search(field,line)[0]+","

    def decode_ss_line(self,line):
        cca = 0
        decoded_line  = ""
        decoded_line += line.split()[cca]+","
        decoded_line += self.add_matched_field('wscale:{} ',line)  # generate two fields !
        decoded_line += self.add_matched_field('rto:{} ',line)
        rtt_temp = self.add_matched_field('rtt:{} ',line)
        decoded_line += rtt_temp.split("/")[0] + "," + rtt_temp.split("/")[1] if not rtt_temp == "NaN" else "NaN"
        decoded_line += self.add_matched_field('mss:{} ',line)
        decoded_line += self.add_matched_field('pmtu:{} ',line)
        decoded_line += self.add_matched_field('rcvmss:{} ',line)
        decoded_line += self.add_matched_field('advmss:{} ',line)
        decoded_line += self.add_matched_field('cwnd:{} ',line)
        decoded_line += self.add_matched_field('ssthresh:{} ',line)
        decoded_line += self.add_matched_field('bytes_sent:{} ',line)
        decoded_line += self.add_matched_field('bytes_acked:{} ',line)
        decoded_line += self.add_matched_field('segs_out:{} ',line)
        decoded_line += self.add_matched_field('segs_in:{} ',line)
        decoded_line += self.add_matched_field('data_segs_out:{} ',line)
        decoded_line += self.add_matched_field('send {}Gbps ',line)
        decoded_line += self.add_matched_field('lastsnd:{} ',line)
        decoded_line += self.add_matched_field('lastrcv:{} ',line)
        decoded_line += self.add_matched_field('pacing_rate {}Gbps ',line)
        decoded_line += self.add_matched_field('delivery_rate {}Gbps ',line)
        decoded_line += self.add_matched_field('delivered:{} ',line)
        decoded_line += self.add_matched_field('busy:{}ms ',line)
        decoded_line += self.add_matched_field('rcv_space:{} ',line)
        decoded_line += self.add_matched_field('rcv_ssthresh:{} ',line)
        decoded_line += self.add_matched_field('notsend:{} ',line) 
        decoded_line += self.add_matched_field('minrtt:{}',line)
        
        return str(decoded_line)+"\n"

    def decode_router_ss_line(self, line):
        qdisc = 1
        decoded_line  = ""
        decoded_line += line.split()[qdisc]+","
        decoded_line += self.add_matched_field('Sent {} bytes',line)
        decoded_line += self.add_matched_field('bytes {} pkt',line)
        decoded_line += self.add_matched_field('dropped {},',line)
        decoded_line += self.add_matched_field('overlimits {} ',line)
        decoded_line += self.add_matched_field('requeues {})',line)
        decoded_line += self.add_matched_field('prob {} ',line)
        decoded_line += self.add_matched_field('delay_c {}us ',line)
        decoded_line += self.add_matched_field('delay_l {}us',line)
        decoded_line += self.add_matched_field('pkts_in_c {} ',line)
        decoded_line += self.add_matched_field('pkts_in_l {} ',line)
        decoded_line += self.add_matched_field('maxq {}e',line)
        decoded_line += self.add_matched_field('ecn_mark {} ',line)
        decoded_line += self.add_matched_field('step_mark {}c',line)
        return str(decoded_line)+"\n"

    def convert_raw_to_csv(self):
        data_exist = Path(self.filename).is_file()
        if self.filename == None:
            print("Object" + str(type(self)) + "has no data to convert (missing data file)")
        elif data_exist is not True:
            print("File {self.filename} does not exists")
        else:
            with open(self.filename+'.csv', 'w') as csv_file, open(self.filename, 'r') as raw_file:
                lines = filter(None, (line.rstrip() for line in raw_file))
                for l in lines:
                    if decode_from_ss:
                        if self.is_router_data():
                            csv_file.write(self.decode_router_ss_line(l))
                        else:
                            csv_file.write(self.decode_ss_line(l))
                    else:
                        csv_file.write(line.replace(" ", ""))
    
    def plot_ss(self):
        self.load_data()
        
        plt.figure()
        r=2
        c=2
        plt.subplot(r, c, 1)
        plt.xlabel("time (in RTT)")
        plt.ylabel("cwnd mean: "+"{:.2f}".format(self.cwnd_mean()))
        plt.plot(self.x, self.cwnd)
        
        plt.subplot(r, c, 2)
        plt.xlabel("time (in RTT)")
        plt.ylabel("Average RTT mean: "+"{:.2f}".format(self.rtt_mean()))
        plt.plot(self.x, self.rtt)
        
        plt.subplot(r, c, 3)
        plt.xlabel("time (in RTT)")
        plt.ylabel("ACKed bytes mean: "+"{:.2f}".format(self.bytes_acked_mean()))
        plt.plot(self.x, self.bytes_acked)
        
        plt.subplot(r, c, 4)
        plt.xlabel("time (in RTT)")
        plt.ylabel("Pacing rate mean: "+"{:.2f}".format(self.pacing_rate_mean()))
        plt.plot(self.x, self.pacing_rate)    
        
        plt.suptitle("Visualisation des résultats")
    
def plot_csv():
    csv = np.genfromtxt(opath+'data.csv', delimiter=",", skip_header=1)

    # Loading part
    x       = np.arange(0,len(csv))

    droprate= csv[:,8]
    markrate= csv[:,9]
    qlen_C  = csv[:,11]
    qlen_L  = csv[:,10]
    
    CC = Measure()
    LC = Measure()
    CS = Measure()
    LS = Measure()
    
    CC.cwnd = csv[:,0]
    CC.mss  = csv[:,1]
    #cwnd_C  = np.multiply(CC.cwnd, CC.mss)
    LC.cwnd = csv[:,2]
    LC.mss  = csv[:,3]
    CS.cwnd = csv[:,4]
    CS.mss  = csv[:,5]
    LS.cwnd = csv[:,6]
    LS.mss  = csv[:,7]

    # Statistics part
    droprate_mean= sum(droprate)/len(droprate)
    markrate_mean= sum(markrate)/len(markrate)
    qlen_C_mean  = sum(qlen_C)/len(qlen_C)
    qlen_L_mean  = sum(qlen_L)/len(qlen_L)
    
    #Visualization part
    r=4
    c=2
    plt.subplot(r, c, 1)
    plt.xlabel("time (in RTT)")
    plt.ylabel("cwnd CC mean: "+"{:.2f}".format(CC.cwnd_mean()))
    plt.plot(x, CC.cwnd)

    plt.subplot(r, c, 2)
    plt.xlabel("time (in RTT)")
    plt.ylabel("cwnd LC mean: "+"{:.2f}".format(LC.cwnd_mean()))
    plt.plot(x, LC.cwnd)

    plt.subplot(r, c, 3)
    plt.xlabel("time (in RTT)")
    plt.ylabel("cwnd CS mean: "+"{:.2f}".format(CS.cwnd_mean()))
    plt.plot(x, CS.cwnd)

    plt.subplot(r, c, 4)
    plt.xlabel("time (in RTT)")
    plt.ylabel("cwnd LS mean: "+"{:.2f}".format(LS.cwnd_mean()))
    plt.plot(x, LS.cwnd)

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

def visualize(rtr_file, atk_file, cc_file, lc_file, cs_file, ls_file):
    
    rtr_measure = Measure(rtr_file)
    atk_measure = Measure(atk_file)
    cc_measure  = Measure(cc_file)
    lc_measure  = Measure(lc_file)
    cs_measure  = Measure(cs_file)
    ls_measure  = Measure(ls_file)
    
    rtr_measure.load_data()
    atk_measure.load_data()
    cc_measure.load_data()
    lc_measure.load_data()
    cs_measure.load_data()
    ls_measure.load_data()
    
    #rtr_measure.plot_ss()
    #atk_measure.plot_ss()
    #cc_measure.plot_ss()
    #lc_measure.plot_ss()
    #cs_measure.plot_ss()
    #ls_measure.plot_ss()
    
    #Visualization part
    fig = plt.figure()
    r=1
    c=2
    
    plt.subplot(r, c, 1)
    plt.ylabel("cwnd evolution")
    plt.plot(atk_measure.x, atk_measure.cwnd, color='r', label='atk Client')
    plt.plot(cc_measure.x, cc_measure.cwnd, color='darkorange', label='Classic Client')
    plt.plot(lc_measure.x, lc_measure.cwnd, color='darkblue', label='LL Client')
    plt.plot(cs_measure.x, cs_measure.cwnd, color='gold', label='Classic Server')
    plt.plot(ls_measure.x, ls_measure.cwnd, color='cyan', label='LL Server')
    
    
    plt.subplot(r, c, 2)
    plt.ylabel("RTT evolution")
    plt.plot(atk_measure.x, atk_measure.rtt, color='r', label='atk')
    plt.plot(cc_measure.x, cc_measure.rtt, color='darkorange', label='Classic Client')
    plt.plot(lc_measure.x, lc_measure.rtt, color='darkblue', label='LL Client')
    plt.plot(cs_measure.x, cs_measure.rtt, color='gold', label='Classic Server')
    plt.plot(ls_measure.x, ls_measure.rtt, color='cyan', label='LL Server')
    
    plt.suptitle("Visualisation des résultats")
    fig.supxlabel("time (in RTT)")
    plt.legend()
    plt.show()

visualize(files["rtr_file"], files["atk_file"], files["cc_file"], files["lc_file"], files["cs_file"], files["ls_file"])
