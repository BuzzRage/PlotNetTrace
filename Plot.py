#!/usr/bin/env python3
import sys
from pathlib import Path
from matplotlib import pyplot as plt
import NetTrace

args   = sys.argv
ipath  = 'data/'
opath  = 'output/'
suffix = ["rtr","atk","cc","lc","cs","ls","rtrvm"]

files               = {}
files["rtr_file"]   = None 
files["atk_file"]   = None
files["cc_file"]    = None
files["lc_file"]    = None
files["cs_file"]    = None
files["ls_file"]    = None
files["rtrvm_file"] = None

verbose = False


def visualize(rtr_file, atk_file, cc_file, lc_file, cs_file, ls_file):
    
    complete = True
    rtr_only = False
    simpletest = False
    cc_with_lc = False
    
    for node in suffix[:-1]:
        if files[node+"_file"] == None: complete = False

    simpletest = True if (files["rtr_file"] != None and files["cc_file"] != None and files["cs_file"] != None and complete is False) else False
    cc_with_lc = True if (files["rtr_file"] != None and files["cc_file"] != None and files["cs_file"] == None) else False
    rtr_only = True if (files["rtr_file"] != None and files["cc_file"] == None and files["cs_file"] == None) else False
    
        
    
    date = rtr_file.split("/")[1]
    timecode = rtr_file.split("/")[2].split("-")[0]
        
    if rtr_only is True:
        rtr_measure = NetTrace.Measure(rtr_file)
        rtr_measure.load_data()
        rtr_measure.plot_all()
        
        plt.suptitle("Measurements: Picoquic tests "+date+" "+timecode)
        plt.show()
        

    if cc_with_lc is True:
    
        rtr_measure = NetTrace.Measure(rtr_file)
        cc_measure  = NetTrace.Measure(cc_file)

        rtr_measure.load_data()
        cc_measure.load_data()
        
        #Visualization part
        fig = plt.figure()
        r=3
        c=3

        
        plt.subplot(r, c, 1)
        plt.ylabel("cwnd evolution")
        plt.plot(cc_measure.x, cc_measure.cwnd*cc_measure.mss, color='darkorange', label='Classic Client')
        plt.legend()
        
        plt.subplot(r, c, 2)
        plt.ylabel("RTT evolution")
        plt.plot(cc_measure.x, cc_measure.rtt, color='darkorange', label='Classic Client')
        plt.legend()
        
        plt.subplot(r, c, 3)
        plt.ylabel("Sending rate (egress Mbps)")
        plt.plot(cc_measure.x, cc_measure.sending_rate, color='darkorange', label='Classic Client')
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
        plt.ylabel("Marking probability (%)")
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
        
        plt.suptitle("Measurements: SimpleTest "+date+" "+timecode)
        fig.supxlabel("time (in ms)")
        plt.show()
        
    if simpletest is True:
    
        rtr_measure = NetTrace.Measure(rtr_file)
        cc_measure  = NetTrace.Measure(cc_file)
        cs_measure  = NetTrace.Measure(cs_file)

        rtr_measure.load_data()
        cc_measure.load_data()
        cs_measure.load_data()
        
        #Visualization part
        fig = plt.figure()
        r=3
        c=3

        
        plt.subplot(r, c, 1)
        plt.ylabel("cwnd evolution")
        plt.plot(cc_measure.x, cc_measure.cwnd*cc_measure.mss, color='darkorange', label='Classic Client')
        plt.plot(cs_measure.x, cs_measure.cwnd*cs_measure.mss, color='gold', label='Classic Server')
        plt.legend()
        
        plt.subplot(r, c, 2)
        plt.ylabel("RTT evolution")
        plt.plot(cc_measure.x, cc_measure.rtt, color='darkorange', label='Classic Client')
        plt.plot(cs_measure.x, cs_measure.rtt, color='gold', label='Classic Server')
        plt.legend()
        
        plt.subplot(r, c, 3)
        plt.ylabel("Sending rate (egress Mbps)")
        plt.plot(cc_measure.x, cc_measure.sending_rate, color='darkorange', label='Classic Client')
        plt.plot(cs_measure.x, cs_measure.sending_rate, color='gold', label='Classic Server')
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
        plt.ylabel("Marking probability (%)")
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
        
        plt.suptitle("Measurements: SimpleTest "+date+" "+timecode)
        fig.supxlabel("time (in ms)")
        plt.show()
        
    if complete is True:
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


if len(args) == 4 and str(args[1]) == "timecode":
    dirpath = ipath + args[2] + "/" + args[3]
    
    for node in suffix:
        filename = dirpath+"-"+node
        node_exist = Path(filename).is_file()
        
        if verbose is True:
            files[node+"_file"] = filename if node_exist is True else print("Warning: file {} does not exist.".format(filename))
        else:
            if node_exist is True: files[node+"_file"] = filename
    
elif len(args) == 7 and str(args[1]) != "timecode":
    
    for f in args[1:]:
        file_exist = Path(f).is_file()
        if file_exist is not True:
            sys.exit(f"File {f} does not exists")
            
    files["rtr_file"] = args[1]
    files["atk_file"] = args[2]
    files["cc_file"]  = args[3]
    files["lc_file"]  = args[4]
    files["cs_file"]  = args[5]
    files["ls_file"]  = args[6]
    
else:
    sys.exit("Invalid arguments. Expected usage:\n"+str(args[0])+" rtr_file atk_file cc_file lc_file cs_file ls_file\nor\n"+str(args[0])+" timecode 2021-05-20 1516\n")
    

visualize(files["rtr_file"], files["atk_file"], files["cc_file"], files["lc_file"], files["cs_file"], files["ls_file"])
