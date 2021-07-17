#!/usr/bin/env python3
import sys
from pathlib import Path
from matplotlib import pyplot as plt
import numpy as np
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


def visualize(rtr_file, atk_file, cc_file, lc_file, cs_file, ls_file, rtrvm_file):
    local_args = locals()
    
    complete     = True
    simpletest   = False
    
    for node in suffix[:-1]:
        if local_args[node+"_file"] == None: complete = False
    
    simpletest = True if (rtr_file != None and cc_file != None and cs_file != None and lc_file == None and complete is False) else False
    downlink   = True if (rtr_file != None and cc_file != None and cs_file != None and lc_file != None and ls_file != None and complete is False) else False
    
    if complete is False and simpletest is False and downlink is False:
        for node in suffix:
            if local_args[node+"_file"] != None:
                unknown_measure = NetTrace.Measure(local_args[node+"_file"])
                unknown_measure.plot_all()
        plt.show()

        
    if simpletest is True or downlink is True or complete is True:
        rtr_measure = NetTrace.Measure(rtr_file)
        cc_measure  = NetTrace.Measure(cc_file)
        cs_measure  = NetTrace.Measure(cs_file)
                
        rtr_measure.load_data()
        cc_measure.load_data()
        cs_measure.load_data()
        
        if simpletest is False:
            lc_measure  = NetTrace.Measure(lc_file)
            ls_measure  = NetTrace.Measure(ls_file)
            lc_measure.load_data()
            ls_measure.load_data()
        
        if complete is True:
            atk_measure = NetTrace.Measure(atk_file)
            atk_measure.load_data()
        
        #Visualization part
        fig = plt.figure()
        
        if not np.isnan(rtr_measure.cpkts[0]):
            r=3
            c=3

            plt.subplot(r, c, 1)
            plt.ylabel("cwnd evolution (MSS)")
            plt.plot(cc_measure.x, cc_measure.cwnd, color='darkorange', label='Classic Client')
            plt.plot(cs_measure.x, cs_measure.cwnd, color='gold', label='Classic Server')
            if simpletest is False:
                plt.plot(lc_measure.x, lc_measure.cwnd, color='darkblue', label='LL Client')
                plt.plot(ls_measure.x, ls_measure.cwnd, color='cyan', label='LL Server')
            
            if complete is True:
                plt.plot(atk_measure.x, atk_measure.cwnd, color='r', label='atk Client')
            plt.legend()
        
            plt.subplot(r, c, 2)
            plt.ylabel("RTT evolution (ms)")
            plt.plot(cc_measure.x, cc_measure.rtt, color='darkorange', label='Classic Client')
            plt.plot(cs_measure.x, cs_measure.rtt, color='gold', label='Classic Server')
            if simpletest is False:
                plt.plot(lc_measure.x, lc_measure.rtt, color='darkblue', label='LL Client')
                plt.plot(ls_measure.x, ls_measure.rtt, color='cyan', label='LL Server')
            if complete is True:
                plt.plot(atk_measure.x, atk_measure.rtt, color='r', label='atk')
            plt.legend()
        
            plt.subplot(r, c, 3)
            plt.ylabel("Sending rate (egress Mbps)")
            plt.plot(cc_measure.x, cc_measure.sending_rate, color='darkorange', label='Classic Client')
            plt.plot(cs_measure.x, cs_measure.sending_rate, color='gold', label='Classic Server')
            if simpletest is False:
                plt.plot(lc_measure.x, lc_measure.sending_rate, color='darkblue', label='LL Client')
                plt.plot(ls_measure.x, ls_measure.sending_rate, color='cyan', label='LL Server')
            if complete is True:
                plt.plot(atk_measure.x, atk_measure.sending_rate, color='r', label='atk')
            plt.legend()
        
            plt.subplot(r, c, 4)
            plt.ylabel("Queue occupation (pkts)")
            plt.plot(rtr_measure.x, rtr_measure.cpkts, color='darkorange', label='Classic pkts')
            plt.plot(rtr_measure.x, rtr_measure.lpkts, color='cyan', label='L4S pkts')
            plt.yscale('log')
            plt.legend()
            
            plt.subplot(r, c, 5)
            plt.ylabel("Queue delay (ms)")
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
        
            plt.suptitle("AQM=DuaplPI2, Timecode: "+date+" "+timecode)
            fig.supxlabel("time (in ms)")
            plt.show()

        else:
            r=2
            c=3
            
            plt.subplot(r, c, 1)
            plt.ylabel("cwnd evolution (MSS)")
            plt.plot(cc_measure.x, cc_measure.cwnd, color='darkorange', label='Classic Client')
            plt.plot(cs_measure.x, cs_measure.cwnd, color='gold', label='Classic Server')
            if simpletest is False:
                plt.plot(lc_measure.x, lc_measure.cwnd, color='darkblue', label='LL Client')
                plt.plot(ls_measure.x, ls_measure.cwnd, color='cyan', label='LL Server')
            
            if complete is True:
                plt.plot(atk_measure.x, atk_measure.cwnd, color='r', label='atk Client')
            plt.legend()
        
            plt.subplot(r, c, 2)
            plt.ylabel("RTT evolution (ms)")
            plt.plot(cc_measure.x, cc_measure.rtt, color='darkorange', label='Classic Client')
            plt.plot(cs_measure.x, cs_measure.rtt, color='gold', label='Classic Server')
            if simpletest is False:
                plt.plot(lc_measure.x, lc_measure.rtt, color='darkblue', label='LL Client')
                plt.plot(ls_measure.x, ls_measure.rtt, color='cyan', label='LL Server')
            if complete is True:
                plt.plot(atk_measure.x, atk_measure.rtt, color='r', label='atk')
            plt.legend()
        
            plt.subplot(r, c, 3)
            plt.ylabel("Sending rate (egress Mbps)")
            plt.plot(cc_measure.x, cc_measure.sending_rate, color='darkorange', label='Classic Client (mean: {:.2f} Mbps)'.format(cc_measure.sending_rate_mean()))
            plt.plot(cs_measure.x, cs_measure.sending_rate, color='gold', label='Classic Server (mean: {:.2f} Mbps)'.format(cs_measure.sending_rate_mean()))
            if simpletest is False:
                plt.plot(lc_measure.x, lc_measure.sending_rate, color='darkblue', label='LL Client (mean: {:.2f} Mbps)'.format(lc_measure.sending_rate_mean()))
                plt.plot(ls_measure.x, ls_measure.sending_rate, color='cyan', label='LL Server (mean: {:.2f} Mbps)'.format(ls_measure.sending_rate_mean()))
            if complete is True:
                plt.plot(atk_measure.x, atk_measure.sending_rate, color='r', label='atk')
            plt.legend()
            
            plt.subplot(r, c, 4)
            plt.ylabel("Pkts sent")
            plt.plot(rtr_measure.x, rtr_measure.pkt_sent, color='green', label='Packets sent')
            plt.legend()
            
            plt.subplot(r, c, 5)
            plt.ylabel("Bytes sent (Average rate: {:.2f} Mbps )".format(rtr_measure.mean_mbps_rate()))
            plt.plot(rtr_measure.x, rtr_measure.bytes_sent, color='green', label='Bytes sent')
            plt.legend()
            
            plt.subplot(r, c, 6)
            plt.ylabel("Pkts dropped and marked")
            plt.plot(rtr_measure.x, rtr_measure.pkt_dropped, color='r', label='Packets dropped')
            plt.legend()
            
            plt.suptitle("AQM=pfifo_fast, Timecode: "+date+" "+timecode)
            fig.supxlabel("time (in ms)")
            plt.show()

if args[1] in ["verbose", "v", "-v"]:
    verbose=True

if "timecode" in [str(args[1]), str(args[2])] and len(args) in range(4,6):
    date = args[-2]
    timecode = args[-1]
    dirpath = ipath + date + "/" + timecode

    for node in suffix:
        filename = dirpath+"-"+node
        node_exist = Path(filename).is_file()
        
        if verbose is True:
            files[node+"_file"] = filename if node_exist is True else print("Info: file {} does not exist.".format(filename))
        else:
            if node_exist is True: files[node+"_file"] = filename
    
elif "timecode" not in [str(args[1]), str(args[2])] and len(args) in range(1,8):
    if Path(args[-1]).is_file() is not True:
        sys.exit(f"File {args[-1]} does not exists")
    date =  args[-1].split("/")[-2]
    timecode = args[-1].split("/")[-1].split("-")[-2]
    
    if verbose is True:
        index = 2
    else:
        index = 1

    for f in args[index:]:
        file_exist = Path(f).is_file()
        if file_exist is not True:
            sys.exit(f"File {f} does not exists")

        for node in suffix:
            if f.split("-")[-1] == node:
                files[node+"_file"] = f
                if verbose is True:
                    print("Info: Loading file {}.".format(f))

else:
    sys.exit("Invalid arguments. Expected usage:\n"+str(args[0])+" rtr_file atk_file cc_file lc_file cs_file ls_file\nor\n"+str(args[0])+" timecode 2021-05-20 1516\n")
    

visualize(files["rtr_file"], files["atk_file"], files["cc_file"], files["lc_file"], files["cs_file"], files["ls_file"], files["rtrvm_file"])


