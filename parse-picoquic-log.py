#!/usr/bin/env python3

import sys
from parse import *
import NetTrace
import matplotlib.pyplot as plt
import numpy as np

## README:
##   parse-picoquic-log.py is a utility that converts logs of picoquic (version draft-17 of QUIC specification) to be compatible with NetTrace data format. 
##   It may also be used as a usage example of NetTrace.


args = list(sys.argv)

def calculate_IAT(raw_name):
    ts_list = list()
    with open(raw_name, 'r') as raw_file:
        raw_file.readline()
        for line in raw_file:
            ts_list.append(float(search("T={} ", line)[0])*1000)
    
    ts_list = np.array(ts_list)
    ts_list = np.diff(ts_list)
    print("Average IAT: {:.2f}ms, min: {:.2f}ms, max: {:.2f}ms, std deviation: {:.2f}ms".format(ts_list.mean(), ts_list.min(), ts_list.max(), ts_list.std(), ts_list.var()))
    return ts_list

def clean_file(log_name,raw_name):
    cpt_line = 0
    full_timestamps = list()
    curr_file = -1
    
    with open(log_name, 'r') as output_log:
        if search("Timestamp={:d}", output_log.readline()) is not None:
            main_ts = float(search("Timestamp={:d}", output_log.readline())[0])
        else: 
            main_ts = float(0)
            
        for line in output_log:           
            if "Timestamp=" in line:
                full_timestamps.append(float(search("Timestamp={:d}", line)[0]))
    
    full_timestamps = np.insert(np.diff(full_timestamps),0,0)/1000000
    full_timestamps = np.cumsum(full_timestamps)
    print(full_timestamps)
    
    with open(raw_name, 'w') as raw_file, open(log_name, 'r') as output_log:
        raw_file.write(output_log.readline())
        for line in output_log:
            if "Timestamp" in line:
                curr_file += 1
                print("file {} ts={}".format(curr_file, full_timestamps[curr_file]))
                
            if "Receiving" in line and "bytes" in line and "MOSAICO" in line:
                ts = float(search("T={} ", line)[0])
                line = line.split("T=")[0]
                line += "T="+str(full_timestamps[curr_file]+ts)+" \n"
                raw_file.write("bytes_acked prague "+line)
                cpt_line += 1
            
    return cpt_line

def convert_raw_to_csv(filename):
    tot_bytes = 0
    current_t = 0
    last_t    = 0
    ts_tare   = int()
        
    with open(filename+'.csv', 'w') as csv_file, open(filename, 'r') as raw_file:
        header = ""

        if search("Timestamp={:d}", raw_file.readline()) is not None:
            timestamp = float(search("Timestamp={:d}", raw_file.readline())[0])/1000
        else:
            timestamp = float(0)
        print(timestamp)

        line = raw_file.readline()
        ts_tare    = float(search("T={} ", line)[0])*1000 + timestamp
        bytes_tare = int(search("Receiving {} bytes", line)[0])
        
        header += "Timestamp: "+str(ts_tare)+", Bytes ACKed counter: "+str(bytes_tare)+", "
        csv_file.write(header+"\n")
        
        for line in raw_file:
            decoded_line = "picoquic-prague,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,\n"
            
            rcv_rate = float(search("rcv_rate_Mbps: {},", line)[0])
            tot_bytes += int(search("Receiving {} bytes", line)[0])
            rtt = float(search("rtt0: {},", line)[0])/1000.0
            current_t = float(search("T={} ", line)[0])*1000
            dt = current_t - last_t
            
            if current_t > 60000-timestamp:
                break
            # Write in .csv with a time step of 20ms
            if dt > 20:
                last_t = current_t
                #decoded_line = decoded_line.replace(",4,", ","+str(rtt)+",")
                decoded_line = decoded_line.replace(",13,", ","+str(tot_bytes-bytes_tare)+",")
                decoded_line = decoded_line.replace(",20,", ","+str(rcv_rate)+",") # /!\ Using pacing_rate placeholder to provide receiving rate calculated by picoquic
                decoded_line = decoded_line.replace(",28,", ","+str(int(ts_tare+current_t))+",")
                csv_file.write(decoded_line)

def plot_measure(raw_fn,cpt_ln):
    measure = NetTrace.Measure(raw_fn)
    measure.load_data(False)
    measure.pacing_rate *= 1000000
    measure.plot_all("Picoquic data")

    plt.figure("Débit picoquic")
    plt.xlabel("time (in RTT)")
    plt.ylabel("Data rate")
    plt.plot(measure.x, measure.pacing_rate, label="Débit instantané (moyenne: {:.2f} Mbps)".format(measure.pacing_rate_mean()), color='cyan')
    plt.plot(measure.x, measure.data_rate, label='Débit sur 1sec (moyenne: {:.2f} Mbps)'.format(measure.data_rate_mean()), color='darkorange')
    plt.legend()
    plt.show()
    
    print("Nb de points pour débit instantané: {:.2f}, nb de points pour débit sur une seconde: {:.2f}, nb de points sur le fichier source: {:.2f}".format(len(measure.pacing_rate), len(measure.data_rate), cpt_ln))

if len(args) > 1:
    log_fn = args[1]
    raw_fn = args[1].split(".raw")[0]
else:
    log_fn = "output.log"
    raw_fn = "0000-uf"

cpt_ln = clean_file(log_fn, raw_fn)
convert_raw_to_csv(raw_fn)

#plot_measure(raw_fn,cpt_ln)
