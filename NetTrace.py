''' NetTrace.py '''

from pathlib import Path
from matplotlib import pyplot as plt
import random
import numpy as np
from parse import *

# Class used to load data and make post-process functions

class Measure:
    def __init__(self, data_file = None):
        self.filename      = data_file
        self.timestamp     = int()
        self.x             = list()

        # Endpoint data
        self.cwnd          = list()
        self.mss           = list()
        self.sending_rate  = list()
        self.rtt           = list()
        self.bytes_acked   = list()
        self.pacing_rate   = list()
        self.delivery_rate = list()
        self.delivered     = list()
        
        # Router data
        self.ecn_tare      = int()
        self.drop_tare     = int()
        self.step_mark_tare= int()
        self.pkt_sent_tare = int()
        self.bytes_sent    = list() 
        self.pkt_sent      = list() 
        self.pkt_dropped   = list() 
        self.pkt_overlimits= list() 
        self.pkt_requeued  = list() 
        self.prob          = list() 
        self.cdelay        = list() 
        self.ldelay        = list() 
        self.cpkts         = list() 
        self.lpkts         = list() 
        self.maxq          = list() 
        self.ecn_mark      = list() 
        self.step_mark     = list() 
        
    def load_data(self):
        f = self.filename+".csv"
        file_exist = Path(f).is_file()
        if file_exist is not True:
            self.convert_raw_to_csv()
        if not self.is_router_data():
            self.load_from_csv()
        elif self.is_router_data():
            self.load_from_router_csv()
        
    def is_router_data(self):
        with open(self.filename, 'r') as f:
            for line in f:
                if "dualpi2" in line or "pfifo_fast" in line:
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
    
    def sending_rate_mean(self):
        return sum(self.sending_rate)/len(self.sending_rate) 
        
    def load_sending_rate(self):
        for i in range(0,len(self.rtt)):
           self.sending_rate[i] = self.cwnd[i]*self.mss[i]*8000000/self.rtt[i]
    
    def conv_to_bps(self,value):
        if value[-1] == 'G':
            return float(value[:-1])*1000000000
        elif value[-1] == 'M':
            return float(value[:-1])*1000000
        elif value[-1] == 'K':
            return float(value[:-1])*1000
        elif value[-1] == 'N':
            return "NaN"
        else:
            return float(value[:-1])
        
    
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
        csv_timestamp      = 28
        
        csv = np.genfromtxt(self.filename+".csv", delimiter=",", skip_header=1)
        self.x             = csv[:,csv_timestamp]
        self.cwnd          = csv[:,csv_cwnd]
        self.mss           = csv[:,csv_mss]
        self.sending_rate  = np.divide(csv[:,csv_send],1000000) # Convert bps to Mbps
        self.rtt           = csv[:,csv_rtt]
        self.bytes_acked   = csv[:,csv_bytes_acked]
        self.pacing_rate   = csv[:,csv_pacing_rate]
        self.delivery_rate = csv[:,csv_delivery_rate]
        self.delivered     = csv[:,csv_delivered]

    def load_from_router_csv(self):
        # Loading part. 
        # See DualPi2 man page for details        
        csv_bytes_sent     = 1  # Bytes sent
        csv_pkt_sent       = 2  # Packets sent
        csv_pkt_dropped    = 3  # Packet dropped
        csv_pkt_overlimits = 4  # Packet overlimits
        csv_pkt_requeued   = 5  # Packet requeued
        csv_prob           = 6  # Probability 
        csv_cdelay         = 7  # Delay on Classic queue 
        csv_ldelay         = 8  # Delay on L4S queue 
        csv_cpkts          = 9  # Packets in Classic queue
        csv_lpkts          = 10  # Packets in L4S queue
        csv_maxq           = 11 # Max packets in queue
        csv_ecn_mark       = 12 # ECN marked packets
        csv_step_mark      = 13 # ???
        csv_timestamp      = 14 # Timestamp
        
        csv = np.genfromtxt(self.filename+".csv", delimiter=",", skip_header=1)
        self.x             = csv[:,csv_timestamp] 
        self.bytes_sent    = csv[:,csv_bytes_sent] 
        self.pkt_sent      = np.array(csv[:,csv_pkt_sent])
        self.pkt_dropped   = np.array(csv[:,csv_pkt_dropped])
        self.pkt_overlimits= csv[:,csv_pkt_overlimits] 
        self.pkt_requeued  = csv[:,csv_pkt_requeued] 
        self.prob          = csv[:,csv_prob]*100               # Convert fraction to %age
        self.cdelay        = np.divide(csv[:,csv_cdelay],1000) # Convert us to ms
        self.ldelay        = np.divide(csv[:,csv_ldelay],1000) # Convert us to ms
        self.cpkts         = csv[:,csv_cpkts] 
        self.lpkts         = csv[:,csv_lpkts] 
        self.maxq          = csv[:,csv_maxq] 
        self.ecn_mark      = np.array(csv[:,csv_ecn_mark])
        self.step_mark     = csv[:,csv_step_mark] 
        
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
        decoded_line += str(self.conv_to_bps(self.add_matched_field('send {}bps ',line)[:-1]))+","
        decoded_line += self.add_matched_field('lastsnd:{} ',line)
        decoded_line += self.add_matched_field('lastrcv:{} ',line)
        decoded_line += str(self.conv_to_bps(self.add_matched_field('pacing_rate {}bps ',line)[:-1]))+","
        decoded_line += str(self.conv_to_bps(self.add_matched_field('delivery_rate {}bps ',line)[:-1]))+","
        decoded_line += self.add_matched_field('delivered:{} ',line)
        decoded_line += self.add_matched_field('busy:{}ms ',line)
        decoded_line += self.add_matched_field('rcv_space:{} ',line)
        decoded_line += self.add_matched_field('rcv_ssthresh:{} ',line)
        decoded_line += self.add_matched_field('notsend:{} ',line) 
        decoded_line += self.add_matched_field('minrtt:{}',line)
        
        # Timestamp calculation
        raw_ts = line.rstrip().split(" ")[-1]
        h  = int(raw_ts.split(":")[0])
        m  = int(raw_ts.split(":")[1])
        s  = int(raw_ts.split(":")[2].split(".")[0])
        ms = int(raw_ts.split(":")[2].split(".")[1])/1000
        t2 = 60*60*1000*h+60*1000*m+1000*s+ms       
        td = t2 - self.timestamp
        decoded_line += str(td)+","
        
        return str(decoded_line)+"\n"

    def decode_router_ss_line(self,line):
        qdisc = line.split()[1]

        decoded_line  = ""
        decoded_line += qdisc+","
        decoded_line += self.add_matched_field('Sent {} bytes',line)
        decoded_line += str(int(self.add_matched_field('bytes {} pkt',line)[:-1])-self.pkt_sent_tare)+","
        decoded_line += str(int(self.add_matched_field('dropped {},',line)[:-1])-self.drop_tare)+","
        decoded_line += self.add_matched_field('overlimits {} ',line)
        decoded_line += self.add_matched_field('requeues {})',line)

        if qdisc == "dualpi2":
            decoded_line += self.add_matched_field('prob {} ',line)
            decoded_line += self.add_matched_field('delay_c {}us ',line)
            decoded_line += self.add_matched_field('delay_l {}us',line)
            decoded_line += self.add_matched_field('pkts_in_c {} ',line)
            decoded_line += self.add_matched_field('pkts_in_l {} ',line)
            decoded_line += self.add_matched_field('maxq {}e',line)
            decoded_line += str(int(self.add_matched_field('ecn_mark {} ',line)[:-1])-self.ecn_tare)+","
            decoded_line += str(int(self.add_matched_field('step_marks {}c',line)[:-1])-self.step_mark_tare)+","
        else:
            decoded_line += ",,,,,,,,"
            
        # Timestamp calculation
        raw_ts = line.rstrip().split(" ")[-1]
        h  = int(raw_ts.split(":")[0])
        m  = int(raw_ts.split(":")[1])
        s  = int(raw_ts.split(":")[2].split(".")[0])
        ms = int(raw_ts.split(":")[2].split(".")[1])
        t2 = 60*60*1000*h+60*1000*m+1000*s+ms       
        td = int(t2 - self.timestamp)
        decoded_line += str(td)+","
        
        return str(decoded_line)+"\n"

    def convert_raw_to_csv(self):
        data_exist = Path(self.filename).is_file()
        if self.filename == None:
            print("Object" + str(type(self)) + "has no data to convert (missing data file)")
        elif data_exist is not True:
            print("File {self.filename} does not exists")
        else:
            with open(self.filename+'.csv', 'w') as csv_file, open(self.filename, 'r') as raw_file:
                lines  = list(filter(None, (line.rstrip() for line in raw_file)))
                header = ""
                
                # Get timestamp and counters
                raw_timestamp  = lines[0].rstrip().split(" ")[-1]
                h  = int(raw_timestamp.split(":")[0])
                m  = int(raw_timestamp.split(":")[1])
                s  = int(raw_timestamp.split(":")[2].split(".")[0])
                ms = int(raw_timestamp.split(":")[2].split(".")[1])
                self.timestamp = 60*60*1000*h+60*1000*m+1000*s+ms/1000
                header += "Timestamp: "+str(self.timestamp)+", "
                
                if self.is_router_data():
                    tmp_ecn_tare        = self.add_matched_field('ecn_mark {} ',lines[0])
                    tmp_drop_tare       = self.add_matched_field('dropped {},',lines[0])
                    tmp_step_mark_tare  = self.add_matched_field('step_marks {}c',lines[0])
                    tmp_pkt_sent_tare   = self.add_matched_field('bytes {} pkt',lines[0])
					
                    # If AQM is DualPI2
                    if len(tmp_ecn_tare) == "NaN,":
                        self.ecn_tare       = int(tmp_ecn_tare[:-1])
                        self.step_mark_tare = int(tmp_step_mark_tare[:-1])
                        header += "ECN Marks counter: "+str(self.ecn_tare)+", "
                        header += "Step marks counter: "+str(self.step_mark_tare)+", "

                    self.drop_tare      = int(tmp_drop_tare[:-1])
                    self.pkt_sent_tare  = int(tmp_pkt_sent_tare[:-1])
                    header += "Dropped Packets counter: "+str(self.drop_tare)+", "
                    header += "Packet counter: "+str(self.pkt_sent_tare)+","
                
                csv_file.write(header+"\n")
                
                for l in lines:      
                    if self.is_router_data():
                        csv_file.write(self.decode_router_ss_line(l))
                    else:
                        csv_file.write(self.decode_ss_line(l))
    
    def plot_all(self, title = "Visualisation de la mesure"):
        self.load_data()
        plt.figure(num=self.filename)
        
        if self.is_router_data():
            r=2
            c=3
            plt.subplot(r, c, 1)
            plt.xlabel("time (in RTT)")
            plt.ylabel("Bytes sent")
            plt.plot(self.x, self.bytes_sent)
            
            plt.subplot(r, c, 2)
            plt.ylabel("Queue occupation (pkts)")
            plt.plot(self.x, self.cpkts, color='darkorange', label='Classic pkts')
            plt.plot(self.x, self.lpkts, color='cyan', label='L4S pkts')
            
            plt.subplot(r, c, 3)
            plt.ylabel("Queue delay")
            plt.plot(self.x, self.cdelay, color='darkorange', label='Classic delay')
            plt.plot(self.x, self.ldelay, color='cyan', label='L4S delay')
            
            plt.subplot(r, c, 4)
            plt.ylabel("Marking and probability (%)")
            plt.plot(self.x, self.prob, color='darkblue', label='Mark probability')
            
            plt.subplot(r, c, 5)
            plt.ylabel("Marked Packets")
            plt.plot(self.x, self.ecn_mark, color='gold', label='ECN Marked packets')
            
            plt.subplot(r, c, 6)
            plt.ylabel("Dropped Packets")
            plt.plot(self.x, self.pkt_dropped, color='r', label='Packets dropped')
            
        else:
            r=3
            c=3

            colors = ["darkblue", "green", "gold", "red", "cyan"]
            random_color = random.choice(colors)

            plt.subplot(r, c, 1)
            plt.xlabel("time (in RTT)")
            plt.ylabel("cwnd mean: "+"{:.2f}".format(self.cwnd_mean()))
            plt.plot(self.x, self.cwnd, color=random_color)

            plt.subplot(r, c, 2)
            plt.xlabel("time (in RTT)")
            plt.ylabel("MSS mean: "+"{:.2f}".format(self.mss_mean()))
            plt.plot(self.x, self.mss, color=random_color)
            
            plt.subplot(r, c, 3)
            plt.xlabel("time (in RTT)")
            plt.ylabel("Average RTT mean: "+"{:.2f}".format(self.rtt_mean()))
            plt.plot(self.x, self.rtt, color=random_color)
            
            plt.subplot(r, c, 4)
            plt.xlabel("time (in RTT)")
            plt.ylabel("ACKed bytes mean: "+"{:.2f}".format(self.bytes_acked_mean()))
            plt.plot(self.x, self.bytes_acked, color=random_color)
            
            plt.subplot(r, c, 5)
            plt.xlabel("time (in RTT)")
            plt.ylabel("Sending rate mean: "+"{:.2f}".format(self.sending_rate_mean()))
            plt.plot(self.x, self.sending_rate, color=random_color)
            
            plt.subplot(r, c, 6)
            plt.xlabel("time (in RTT)")
            plt.ylabel("Pacing rate mean: "+"{:.2f}".format(self.pacing_rate_mean()))
            plt.plot(self.x, self.pacing_rate, color=random_color)
            
            plt.subplot(r, c, 7)
            plt.xlabel("time (in RTT)")
            plt.ylabel("Delivered packets")
            plt.plot(self.x, self.delivered, color=random_color)
        
        plt.suptitle(title)
