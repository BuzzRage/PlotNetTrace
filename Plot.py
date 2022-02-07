''' Plot.py '''

from matplotlib import pyplot as plt
import numpy as np
import NetTrace

# This file contains Plotting functions
class Plot:
    def __init__(self, date, timecode, rtr_file, atk_file, cc_file, lc_file, cs_file, ls_file, rtrvm_file, rewrite_mode=False):
        self.date       = date
        self.timecode   = timecode
        self.files      = {"rtr_file":rtr_file, "atk_file":atk_file, "cc_file":cc_file, "lc_file":lc_file, "cs_file":cs_file, "ls_file":ls_file, "rtrvm_file":rtrvm_file}
        self.complete   = False
        self.c_flows = False
        self.l_flows    = False
        self.downlink   = False
        self.rewriteCSV = rewrite_mode
        self.suffix     = ["rtr","atk","cc","lc","cs","ls","rtrvm"]
    def load_testbed_type(self):
        complete = True
        
        for node in self.suffix[:-1]:
            if self.files[node+"_file"] == None: complete = False
            
        self.complete   = complete
        self.c_flows = True if (self.files["rtr_file"] != None and self.files["cc_file"] != None and self.files["cs_file"] != None and self.files["lc_file"] == None) else False
        self.l_flows    = True if (self.files["rtr_file"] != None and self.files["cc_file"] == None and self.files["cs_file"] == None and self.files["lc_file"] != None and self.files["ls_file"] != None) else False
        self.downlink   = True if (self.files["rtr_file"] != None and self.files["cc_file"] != None and self.files["cs_file"] != None and self.files["lc_file"] != None and self.files["ls_file"] != None and self.complete is False) else False
    
    def visualize(self):
        self.load_testbed_type()
        
        if self.c_flows is True or self.downlink is True or self.complete is True or self.l_flows is True:
            rtr_measure = NetTrace.Measure(self.files["rtr_file"])
            rtr_measure.load_data(self.rewriteCSV)
            
            if self.l_flows is not True:
                cc_measure = NetTrace.Measure(self.files["cc_file"])
                cs_measure = NetTrace.Measure(self.files["cs_file"])
                cc_measure.load_data(self.rewriteCSV)
                cs_measure.load_data(self.rewriteCSV)

            if self.c_flows is not True:
                lc_measure = NetTrace.Measure(self.files["lc_file"])
                ls_measure = NetTrace.Measure(self.files["ls_file"])
                lc_measure.load_data(self.rewriteCSV)
                ls_measure.load_data(self.rewriteCSV)
            
            if self.complete is True:
                atk_measure = NetTrace.Measure(self.files["atk_file"])
                atk_measure.load_data(self.rewriteCSV)
            
            #Visualization part
            fig = plt.figure()

            if rtr_measure.AQM_is_L4S is True:
                r=3
                c=3
            else:
                r=2
                c=3

            plt.subplot(r, c, 1)
            plt.ylabel("cwnd evolution (MSS)")
            if self.l_flows is not True:
                plt.plot(cs_measure.x, cs_measure.cwnd, color='gold', label='Classic Server')
            if self.c_flows is not True:
                plt.plot(ls_measure.x, ls_measure.cwnd, color='cyan', label='LL Server')
            if self.complete is True:
                plt.plot(atk_measure.x, atk_measure.cwnd, color='r', label='atk Client')
            plt.legend()
        
            plt.subplot(r, c, 2)
            plt.ylabel("RTT evolution (ms)")
            if self.l_flows is not True:
                plt.plot(cs_measure.x, cs_measure.rtt, color='gold', label='Classic Server')
            if self.c_flows is not True:
                plt.plot(ls_measure.x, ls_measure.rtt, color='cyan', label='LL Server')
            if self.complete is True:
                plt.plot(atk_measure.x, atk_measure.rtt, color='r', label='atk')
            plt.legend()

            plt.subplot(r, c, 3)
            plt.ylabel("Sending rate (egress Mbps)")
            if self.l_flows is not True:
                plt.plot(cc_measure.x, cc_measure.sending_rate, color='darkorange', label='Classic Client (mean: {:.2f} Mbps)'.format(cc_measure.mean_mbps_rate()))
                plt.plot(cs_measure.x, cs_measure.sending_rate, color='gold', label='Classic Server (mean: {:.2f} Mbps)'.format(cs_measure.mean_mbps_rate()))
                plt.plot(cs_measure.x, cs_measure.data_rate, color='red', label='CS data rate (mean: {:.2f} Mbps)'.format(cs_measure.data_rate_mean()))

            if self.c_flows is not True:
                plt.plot(ls_measure.x, ls_measure.sending_rate, color='cyan', label='LL Server (mean: {:.2f} Mbps)'.format(ls_measure.mean_mbps_rate()))
                plt.plot(ls_measure.x, ls_measure.data_rate, color='green', label='LS data rate (mean: {:.2f} Mbps)'.format(ls_measure.data_rate_mean()))
            if self.complete is True:
                plt.plot(atk_measure.x, atk_measure.sending_rate, color='r', label='atk')
            plt.legend(loc="lower right", prop={'size': 6})


            if rtr_measure.AQM_is_L4S is True:
                ax1 = plt.subplot(r, c, 4)
                plt.ylabel("Queue occupation (pkts)")
                plot1 = ax1.plot(rtr_measure.x, rtr_measure.cpkts_t, color='darkorange', label='Classic pkts')
                plot2 = ax1.plot(rtr_measure.x, rtr_measure.lpkts_t, color='cyan', label='L4S pkts')
                
                ax2 = ax1.twinx() 
                plot3 = ax2.plot(rtr_measure.x, rtr_measure.qoccupation, color='red', label='Saturation ratio')
                ax2.tick_params(axis ='y', labelcolor = 'black') 
                
                plots = plot1 + plot2 + plot3
                labels = [l.get_label() for l in plots]
                plt.legend(plots, labels, loc=0)

                plt.subplot(r, c, 5)
                plt.ylabel("Queue delay (ms)")
                plt.plot(rtr_measure.x, rtr_measure.cdelay, '.', color='darkorange', label='Classic delay')
                plt.plot(rtr_measure.x, rtr_measure.ldelay, '.', color='cyan', label='L4S delay')
                plt.yscale('log')
                plt.legend()

                plt.subplot(r, c, 6)
                plt.ylabel("Marking probability (%)")
                plt.plot(rtr_measure.x, rtr_measure.prob, color='darkblue')

                plt.subplot(r, c, 7)
                plt.ylabel("Bytes sent (Average rate: {:.2f} Mbps )".format(rtr_measure.mean_mbps_rate()))
                plt.plot(rtr_measure.x, rtr_measure.bytes_sent_t, color='green')

                plt.subplot(r, c, 8)
                plt.ylabel("Dropped Packets (Total: {})".format(rtr_measure.pkt_dropped[-1]))
                plt.plot(rtr_measure.x, rtr_measure.pkt_dropped_t, color='r')

                plt.subplot(r, c, 9)
                plt.ylabel("ECN Marked packets\n Total: {} ECN marks\n {} step marks".format(rtr_measure.ecn_mark[-1], rtr_measure.step_mark[-1])) 
                plt.plot(rtr_measure.x, rtr_measure.ecn_mark_t, color='gold', label='aqm marks (PI² + kp)')
                plt.plot(rtr_measure.x, rtr_measure.step_mark_t, color='#80B280', label='step marks')
                plt.legend()

                plt.suptitle("AQM=DuaplPI2, Timecode: "+self.date+" "+self.timecode)
                fig.supxlabel("time (in ms)")
                plt.gcf().subplots_adjust(
                    left=0.045,
                    bottom=0.06,
                    right=0.99,
                    top=0.95,
                    wspace=0.220,
                    hspace=0.20
                )
                plt.show()

            else:
                plt.subplot(r, c, 4)
                plt.ylabel("Packets sent")
                plt.plot(rtr_measure.x, rtr_measure.pkt_sent, color='green')

                plt.subplot(r, c, 5)
                plt.ylabel("Bytes sent (Average rate: {:.2f} Mbps )".format(rtr_measure.mean_mbps_rate()))
                plt.plot(rtr_measure.x, rtr_measure.bytes_sent, color='green')

                plt.subplot(r, c, 6)
                plt.ylabel("Dropped Packets")
                plt.plot(rtr_measure.x, rtr_measure.pkt_dropped, color='r')

                plt.suptitle("AQM=pfifo_fast, Timecode: "+self.date+" "+self.timecode)
                fig.supxlabel("time (in ms)")
                plt.show()

        else:
            for node in self.suffix:
                if self.files[node+"_file"] != None:
                    unknown_measure = NetTrace.Measure(self.files[node+"_file"])
                    unknown_measure.plot_all()
            plt.show()

    def timefreq_plot(self):
        self.load_testbed_type()

        rtr_measure = NetTrace.Measure(self.files["rtr_file"])
        ls_measure = NetTrace.Measure(self.files["ls_file"])
        rtr_measure.load_data(self.rewriteCSV)
        ls_measure.load_data(self.rewriteCSV)


        #Visualization part
        fig = plt.figure()
        r=3
        c=2

        plt.subplot(r, c, 1)
        plt.ylabel("RTT evolution (ms)")
        plt.xlabel("time (in ms)")
        plt.plot(ls_measure.x, ls_measure.rtt, color='green')
        plt.grid()

        plt.subplot(r, c, 2)
        plt.ylabel("RTT value occurrency")
        plt.hist(ls_measure.rtt, bins=np.arange(min(ls_measure.rtt),max(ls_measure.rtt)), density=False, color='blue')
        plt.grid()

        plt.subplot(r, c, 3)
        plt.ylabel("Sending rate (Mbps)")
        plt.xlabel("time (in ms)")
        plt.plot(ls_measure.x, ls_measure.sending_rate, color='blue', label='egress rate (mean: {:.2f} Mbps)'.format(ls_measure.mean_mbps_rate()))
        plt.plot(ls_measure.x, ls_measure.data_rate, color='red', label='data rate (mean: {:.2f} Mbps)'.format(ls_measure.data_rate_mean()))
        plt.legend(loc="upper right", prop={'size': 8})
        plt.grid()

        plt.subplot(r, c, 4)
        plt.ylabel("Sending rate value occurrency")
        interval = np.arange(min(ls_measure.sending_rate),max(ls_measure.sending_rate),0.2)
        plt.hist(ls_measure.sending_rate, bins=interval, density=False, color='blue')
        plt.hist(ls_measure.data_rate, bins=np.arange(min(ls_measure.data_rate),max(ls_measure.data_rate),0.2), density=False, color='red')
        plt.grid()

        plt.subplot(r, c, 5)
        plt.ylabel("lqueue delay (ms)")
        plt.plot(rtr_measure.x, rtr_measure.ldelay, '.', color='green')
        plt.yscale('log')
        plt.xlabel("time (in ms)")
        plt.grid()

        plt.subplot(r, c, 6)
        plt.ylabel("lqueue delay value occurrency")
        plt.hist(rtr_measure.ldelay, bins=np.arange(min(rtr_measure.ldelay),max(rtr_measure.ldelay)), density=False, color='blue')
        plt.grid()


        plt.show()
        
    def special_plot(self):
        self.load_testbed_type()

        rtr_measure = NetTrace.Measure(self.files["rtr_file"])
        ls_measure = NetTrace.Measure(self.files["ls_file"])
        rtr_measure.load_data(self.rewriteCSV)
        ls_measure.load_data(self.rewriteCSV)


        #Visualization part
        fig = plt.figure()
        r=3
        c=2

        plt.subplot(r, c, 1)
        plt.ylabel("RTT evolution (ms)")
        plt.xlabel("time (in ms)")
        plt.plot(ls_measure.x, ls_measure.rtt, color='green')
        plt.grid()

        plt.subplot(r, c, 2)
        plt.ylabel("Marking probability (%)")
        plt.plot(rtr_measure.x, rtr_measure.prob, color='darkblue')
        plt.grid()
        
        plt.subplot(r, c, 3)
        plt.ylabel("Sending rate (Mbps)")
        plt.xlabel("time (in ms)")
        plt.plot(ls_measure.x, ls_measure.sending_rate, color='blue', label='egress rate (mean: {:.2f} Mbps)'.format(ls_measure.mean_mbps_rate()))
        plt.plot(ls_measure.x, ls_measure.data_rate, color='red', label='data rate (mean: {:.2f} Mbps)'.format(ls_measure.data_rate_mean()))
        plt.legend(loc="upper right", prop={'size': 8})
        plt.grid()

        plt.subplot(r, c, 4)
        plt.ylabel("Dropped Packets")
        plt.plot(rtr_measure.x, rtr_measure.pkt_dropped, color='r')
        plt.grid()
        
        plt.subplot(r, c, 5)
        plt.ylabel("lqueue delay (ms)")
        plt.plot(rtr_measure.x, rtr_measure.ldelay, '.', color='green')
        plt.yscale('log')
        plt.xlabel("time (in ms)")
        plt.grid()

        plt.subplot(r, c, 6)
        plt.ylabel("ECN Marked packets")
        plt.plot(rtr_measure.x, rtr_measure.step_mark, color='#80B280', label='step marks')
        plt.plot(rtr_measure.x, rtr_measure.ecn_mark, color='gold', label='aqm marks (PI² + kp)')
        plt.legend()
        plt.grid()
        
        plt.show()


    def multiexp_plot(self, path):

        #experiences = {'000': None, '001': "1653", '010': "1712", '011': "1707", '100': None, '101': "1648", '110': "1740", '111': "1724"}
        #experiences = {'000': "1722", '001': "1725", '010': "1734", '011': "1731", '100': "1805", '101': "1746", '110': "1808", '111': "1749"}
        #experiences = {'U\u0304E\u0304+B\u0304+P\u0304': "1722", 'U\u0304E\u0304+B\u0304+P': "1725", 'U\u0304E\u0304+B+P\u0304': "1734", 'U\u0304E\u0304+B+B': "1731", 'UE+B\u0304+P\u0304': "1805", 'UE+B\u0304+P': "1746", 'UE+B+P\u0304': "1808", 'UE+B+P': "1749"}
        #experiences = {'001': "1653", '010': "1712", '011': "1707", '101': "1648", '110': "1740", '111': "1724"}
        #rtr_data    = {experiences[0]: rtr[0], experiences[1]: rtr[1], experiences[2]: rtr[2], experiences[3]: rtr[3], experiences[4]: rtr[4], experiences[5]: rtr[5]}
        
        experiences = {'Normal': "1612", 'Unresponsive \nECN': "1746", 'Bursts': "1734", 'No pacing': "1722"}
        
        rtr_data    = dict()
        lflow_data  = dict()
        
        for exp in experiences.keys():
            if experiences[exp]:
                rtr_data[exp]   = NetTrace.Measure(path+experiences[exp]+"-rtr")
                lflow_data[exp] = NetTrace.Measure(path+experiences[exp]+"-ls")
                rtr_data[exp].load_data(self.rewriteCSV)
                lflow_data[exp].load_data(self.rewriteCSV)
                
        r = 2
        c = 3
        rotat_val = 15
        fig = plt.figure()
        
        plt.subplot(r, c, 1)
        plt.boxplot([lflow_data[x].rtt for x in experiences.keys()], labels = experiences.keys(), showfliers=False)
        plt.ylabel("(a) RTT (ms)")
        plt.ylim(ymin=0)
        plt.xticks(rotation=rotat_val)
        plt.grid()
        
        plt.subplot(r, c, 2)
        plt.boxplot([lflow_data[x].sending_rate for x in experiences.keys()], labels = experiences.keys(), showfliers=False)
        plt.ylabel("(b) Sending rate \n(Mbps)")
        plt.ylim(ymin=0)
        plt.xticks(rotation=rotat_val)
        plt.grid()
        
        #plt.subplot(r, c, 3)
        #plt.boxplot([lflow_data[x].rttvar for x in experiences.keys()], labels = experiences.keys(), showfliers=False)
        #plt.ylabel("Mean deviation of RTT")
        #plt.xticks(rotation=rotat_val)
        #plt.grid()

#Scaling:         
#top=0.995,
#bottom=0.54,
#left=0.03,
#right=0.61,
#hspace=0.36,
#wspace=0.315
        
        plt.subplot(r, c, 3)
        plt.boxplot([rtr_data[x].ldelay for x in experiences.keys()], labels = experiences.keys(), showfliers=False)
        plt.ylabel("(c) Queuing delay of \nLL queue (ms)")
        plt.xticks(rotation=rotat_val)
        plt.grid()
        
        plt.subplot(r, c, 4)
        plt.boxplot([rtr_data[x].prob for x in experiences.keys()], labels = experiences.keys(), showfliers=False)
        plt.ylabel("(d) Marking probability (%)")
        plt.xticks(rotation=rotat_val)
        plt.grid()
        
        plt.subplot(r, c, 5)
        plt.boxplot([rtr_data[x].pkt_dropped for x in experiences.keys()], labels = experiences.keys(), showfliers=False)
        plt.ylabel("(e) Dropped packets")
        plt.xticks(rotation=rotat_val)
        plt.grid()
        
        plt.subplot(r, c, 6)
        plt.boxplot([rtr_data[x].ecn_mark for x in experiences.keys()], labels = experiences.keys(), showfliers=False)
        plt.ylabel("(f) Marked packets")
        plt.xticks(rotation=rotat_val)
        plt.grid()
        
        plt.gcf().subplots_adjust(left=0.03,bottom=0.54,right=0.61,top=0.995,wspace=0.315,hspace=0.36)
        plt.show()

        
        #ls_measure.lastsnd
