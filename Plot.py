#!/usr/bin/env python3
import sys
from pathlib import Path
from matplotlib import pyplot as plt
import NetTrace

ipath          = 'data/'
opath          = 'output/'

args  = sys.argv
files = {}

filenames = list()
if len(args) == 4 and str(args[1]) == "timecode":
    dirpath = ipath + args[2] + "/" + args[3]
    

    filenames.append(dirpath+"-rtr")
    filenames.append(dirpath+"-atk")
    filenames.append(dirpath+"-cc")
    filenames.append(dirpath+"-lc")
    filenames.append(dirpath+"-cs")
    filenames.append(dirpath+"-ls")
elif len(args) == 7 and str(args[1]) != "timecode":
    filenames.append(args[1])
    filenames.append(args[2])
    filenames.append(args[3])
    filenames.append(args[4])
    filenames.append(args[5])
    filenames.append(args[6])
else :
    sys.exit("Invalid arguments. Expected usage:\n"+str(args[0])+" rtr_file atk_file cc_file lc_file cs_file ls_file\nor\n"+str(args[0])+" timecode 2021-05-20 1516\n")
for f in filenames:
    file_exist = Path(f).is_file()
    if file_exist is not True:
        sys.exit(f"File {f} does not exists")
        
files["rtr_file"] = filenames[0]
files["atk_file"] = filenames[1]
files["cc_file"]  = filenames[2]
files["lc_file"]  = filenames[3]
files["cs_file"]  = filenames[4]
files["ls_file"]  = filenames[5]
    
def visualize(rtr_file, atk_file, cc_file, lc_file, cs_file, ls_file):
    
    rtr_measure = NetTrace.Measure(rtr_file)
    atk_measure = NetTrace.Measure(atk_file)
    cc_measure  = NetTrace.Measure(cc_file)
    lc_measure  = NetTrace.Measure(lc_file)
    cs_measure  = NetTrace.Measure(cs_file)
    ls_measure  = NetTrace.Measure(ls_file)
    
    rtr_measure.load_data()
    atk_measure.load_data()
    cc_measure.load_data()
    lc_measure.load_data()
    cs_measure.load_data()
    ls_measure.load_data()
    
    
    #Visualization part
    fig = plt.figure()
    r=3
    c=3

    
    plt.subplot(r, c, 1)
    plt.ylabel("cwnd evolution")
    plt.plot(atk_measure.x, atk_measure.cwnd*atk_measure.mss, color='r', label='atk Client')
    plt.plot(cc_measure.x, cc_measure.cwnd*cc_measure.mss, color='darkorange', label='Classic Client')
    plt.plot(lc_measure.x, lc_measure.cwnd*lc_measure.mss, color='darkblue', label='LL Client')
    plt.plot(cs_measure.x, cs_measure.cwnd*cs_measure.mss, color='gold', label='Classic Server')
    plt.plot(ls_measure.x, ls_measure.cwnd*ls_measure.mss, color='cyan', label='LL Server')
    plt.legend()
    
    plt.subplot(r, c, 2)
    plt.ylabel("RTT evolution")
    plt.plot(atk_measure.x, atk_measure.rtt, color='r', label='atk')
    plt.plot(cc_measure.x, cc_measure.rtt, color='darkorange', label='Classic Client')
    plt.plot(lc_measure.x, lc_measure.rtt, color='darkblue', label='LL Client')
    plt.plot(cs_measure.x, cs_measure.rtt, color='gold', label='Classic Server')
    plt.plot(ls_measure.x, ls_measure.rtt, color='cyan', label='LL Server')
    plt.legend()
    
    plt.subplot(r, c, 3)
    plt.ylabel("Sending rate (egress Mbps)")
    plt.plot(atk_measure.x, atk_measure.sending_rate, color='r', label='atk')
    plt.plot(cc_measure.x, cc_measure.sending_rate, color='darkorange', label='Classic Client')
    plt.plot(lc_measure.x, lc_measure.sending_rate, color='darkblue', label='LL Client')
    plt.plot(cs_measure.x, cs_measure.sending_rate, color='gold', label='Classic Server')
    plt.plot(ls_measure.x, ls_measure.sending_rate, color='cyan', label='LL Server')
    plt.legend()
    
    plt.subplot(r, c, 4)
    plt.ylabel("Queue occupation")
    plt.plot(rtr_measure.x, rtr_measure.cpkts, color='darkorange', label='Classic pkts')
    plt.plot(rtr_measure.x, rtr_measure.lpkts, color='cyan', label='L4S pkts')
    plt.yscale('log')
    plt.legend()
    
    plt.subplot(r, c, 5)
    plt.ylabel("Queue delay")
    plt.plot(rtr_measure.x, rtr_measure.cdelay, color='darkorange', label='Classic delay')
    plt.plot(rtr_measure.x, rtr_measure.ldelay, color='cyan', label='L4S delay')
    plt.yscale('log')
    plt.legend()
    
    plt.subplot(r, c, 6)
    plt.ylabel("Marking and probability")
    plt.plot(rtr_measure.x, rtr_measure.prob, color='darkblue', label='Mark probability')
    plt.legend()
    
    plt.subplot(r, c, 7)
    plt.ylabel("Pkts sent")
    plt.plot(rtr_measure.x, rtr_measure.pkt_sent, color='green', label='Packets sent')
    plt.legend()
    
    plt.subplot(r, c, 8)
    plt.ylabel("Step marks")
    plt.plot(rtr_measure.x, rtr_measure.step_mark, color='r', label='Step marks')
    plt.legend()
    
    plt.subplot(r, c, 9)
    plt.ylabel("Pkts dropped and marked")
    plt.plot(rtr_measure.x, rtr_measure.pkt_dropped, color='r', label='Packets dropped')
    plt.plot(rtr_measure.x, rtr_measure.ecn_mark, color='gold', label='ECN Marked packets')
    plt.legend()
    
    plt.suptitle("Visualisation des résultats")
    fig.supxlabel("time (in ms)")
    plt.show()

visualize(files["rtr_file"], files["atk_file"], files["cc_file"], files["lc_file"], files["cs_file"], files["ls_file"])
