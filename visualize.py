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
        # à revoir: les données changent
        cca            = 0 # Constant
        # wscale         = 1 # <snd_wscale>:<rcv_wscale>
        # rto            = 2
        # rtt            = 3 # Gives average RTT / mean RTTVAR
        # mss            = 4 
        # pmtu           = 5
        # rcvmss         = 6
        # advmss         = 7
        # cwnd           = 8
        # ssthresh       = 9
        # bytes_sent     = 10
        # bytes_acked    = 11
        # segs_out       = 12
        # segs_in        = 13
        # data_segs_out  = 14
        # send           = 16 # 15 string ; 16 value
        # lastsnd        = 17
        # lastrcv        = 18
        # pacing_rate    = 20 # 19 string ; 20 value
        # delivery_rate  = 22 # 21 string ; 22 value
        # delivered      = 23
        # busy           = 24
        # unacked        = 24
        # rcv_space      = 25
        # rcv_thresh     = 26
        # notsent        = 27
        # minrtt         = 28
        
        
        
else:
    finput = ipath+'data.raw'

def add_matched_filed(field,line):
    return "NaN," if not search(field,line) else search(field,line)[0]+","

def decode_ss_line(line):
    #print(line)
    decoded_line  = ""
    decoded_line += line.split()[cca]+","
    decoded_line += add_matched_filed('wscale:{} ',line)  # génère deux champs !
    decoded_line += add_matched_filed('rto:{} ',line)
    rtt_temp = add_matched_filed('rtt:{} ',line)
    decoded_line += rtt_temp.split("/")[0] + "," + rtt_temp.split("/")[1] if not rtt_temp == "NaN" else "NaN"
    decoded_line += add_matched_filed('mss:{} ',line)
    decoded_line += add_matched_filed('pmtu:{} ',line)
    decoded_line += add_matched_filed('rcvmss:{} ',line)
    decoded_line += add_matched_filed('advmss:{} ',line)
    decoded_line += add_matched_filed('cwnd:{} ',line)
    decoded_line += add_matched_filed('ssthresh:{} ',line)
    decoded_line += add_matched_filed('bytes_sent:{} ',line)
    decoded_line += add_matched_filed('bytes_acked:{} ',line)
    decoded_line += add_matched_filed('segs_out:{} ',line)
    decoded_line += add_matched_filed('segs_in:{} ',line)
    decoded_line += add_matched_filed('data_segs_out:{} ',line)
    decoded_line += add_matched_filed('send {}Gbps ',line)
    decoded_line += add_matched_filed('lastsnd:{} ',line)
    decoded_line += add_matched_filed('lastrcv:{} ',line)
    decoded_line += add_matched_filed('pacing_rate {}Gbps ',line)
    decoded_line += add_matched_filed('delivery_rate {}Gbps ',line)
    decoded_line += add_matched_filed('delivered:{} ',line)
    decoded_line += add_matched_filed('busy:{}ms ',line)
    decoded_line += add_matched_filed('rcv_space:{} ',line)
    decoded_line += add_matched_filed('rcv_ssthresh:{} ',line)
    decoded_line += add_matched_filed('notsend:{} ',line) 
    decoded_line += add_matched_filed('minrtt:{}',line)
    
    # decoded_line += line.split()[wscale].split(":")[1].split(",")[0]+","+line.split()[wscale].split(":")[1].split(",")[1]+","
    # decoded_line += line.split()[rto].split(":")[1]+","
    # decoded_line += line.split()[rtt].split(":")[1].split("/")[0]+","+line.split()[rtt].split(":")[1].split("/")[1]+","
    # decoded_line += line.split()[mss].split(":")[1]+","
    # decoded_line += line.split()[pmtu].split(":")[1]+","
    # decoded_line += line.split()[rcvmss].split(":")[1]+","
    # decoded_line += line.split()[advmss].split(":")[1]+","
    # decoded_line += line.split()[cwnd].split(":")[1]+","
    # decoded_line += line.split()[ssthresh].split(":")[1]+","
    # decoded_line += line.split()[bytes_sent].split(":")[1]+","
    # decoded_line += line.split()[bytes_acked].split(":")[1]+","
    # decoded_line += line.split()[segs_out].split(":")[1]+","
    # decoded_line += line.split()[segs_in].split(":")[1]+","
    # decoded_line += line.split()[data_segs_out].split(":")[1]+","
    # decoded_line += line.split()[send].split("G")[0]+","
    # decoded_line += line.split()[lastrcv].split(":")[1]+","
    # decoded_line += line.split()[pacing_rate].split("G")[0]+","
    # decoded_line += line.split()[delivery_rate].split("G")[0]+","
    # decoded_line += line.split()[delivered].split(":")[1]+","
    # decoded_line += line.split()[busy].split(":")[1].split("m")[0]+","
    # decoded_line += line.split()[unacked].split(":")[1]+","
    # decoded_line += line.split()[rcv_space].split(":")[1]+","
    # decoded_line += line.split()[rcv_thresh].split(":")[1]+","
    # decoded_line += line.split()[notsent].split(":")[1]+","
    # decoded_line += line.split()[minrtt].split(":")[1]+","
    #print(decoded_line)
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
    csv = np.genfromtxt(opath+'data.csv', delimiter=",", skip_header=1)
    
    # Loading part
    csv_cca            = 0 # Constant
    csv_wscale1        = 1 # <snd_wscale>
    csv_wscale2        = 2 # <rcv_wscale>
    csv_rto            = 3
    csv_rtt            = 4 # average RTT / mean RTTVAR
    csv_rttvar         = 5 # mean RTTVAR
    csv_mss            = 6
    csv_pmtu           = 7
    csv_rcvmss         = 8
    csv_advmss         = 9
    csv_cwnd           = 10
    csv_ssthresh       = 11
    csv_bytes_sent     = 12
    csv_bytes_acked    = 13
    csv_segs_out       = 14
    csv_segs_in        = 15
    csv_data_segs_out  = 16
    csv_send           = 17
    csv_lastsnd        = 18
    csv_lastrcv        = 19
    csv_pacing_rate    = 20 
    csv_delivery_rate  = 21
    csv_delivered      = 22
    csv_busy           = 23
    csv_unacked        = 23 # non parsé
    csv_rcv_space      = 24
    csv_rcv_thresh     = 25
    csv_notsent        = 26
    csv_minrtt         = 27
    
    x           = np.arange(0,len(csv))
    cwnd_CC     = csv[:,csv_cwnd]
    MSS_CC      = csv[:,csv_mss]
    RTT         = csv[:,csv_rtt]
    cwnd_C      = np.multiply(cwnd_CC, MSS_CC)
    bytes_acked = csv[:,csv_bytes_acked]
    pacing_rate = csv[:,csv_pacing_rate]
    
    # Statistics part
    cwnd_CC_mean     = sum(cwnd_CC)/len(cwnd_CC)
    MSS_CC_mean      = sum(MSS_CC)/len(MSS_CC)
    RTT_mean         = sum(RTT)/len(RTT)
    bytes_acked_mean = sum(bytes_acked)/len(bytes_acked)
    pacing_rate_mean = sum(pacing_rate)/len(pacing_rate)
    
    #Visualization part
    r=2
    c=2
    plt.subplot(r, c, 1)
    plt.xlabel("time (in RTT)")
    plt.ylabel("cwnd CC mean: "+"{:.2f}".format(cwnd_CC_mean))
    plt.plot(x, cwnd_CC)
    
    plt.subplot(r, c, 2)
    plt.xlabel("time (in RTT)")
    plt.ylabel("Average RTT mean: "+"{:.2f}".format(RTT_mean))
    plt.plot(x, RTT)
    
    plt.subplot(r, c, 3)
    plt.xlabel("time (in RTT)")
    plt.ylabel("ACKed bytes mean: "+"{:.2f}".format(bytes_acked_mean))
    plt.plot(x, bytes_acked)
    
    plt.subplot(r, c, 4)
    plt.xlabel("time (in RTT)")
    plt.ylabel("Pacing rate mean: "+"{:.2f}".format(pacing_rate_mean))
    plt.plot(x, pacing_rate)    
    
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
