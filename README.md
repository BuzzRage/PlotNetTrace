# PlotNetTrace

A tool to parse and analyse raw ss (Socket Statistics) output from a device (endpoint or router).

Input file should be raw ss lines. For example with `ss -pti | grep -A1 "firefox" | tail -n1` it gives:
```
         cubic wscale:8,7 rto:226.666 rtt:25.501/8.796 ato:40 mss:1428 pmtu:1500 rcvmss:1208 advmss:1428 cwnd:10 bytes_sent:1113 bytes_acked:1114 bytes_received:38288 segs_out:34 segs_in:41 data_segs_out:7 data_segs_in:36 send 4.48Mbps lastsnd:58214 lastrcv:58197 lastack:58197 pacing_rate 8.96Mbps delivery_rate 1.19Mbps delivered:8 app_limited busy:109ms rcv_rtt:19.472 rcv_space:22525 rcv_ssthresh:65346 minrtt:17.24
```

For router data, `tc -s qdisc show dev <your device> | tr -d "\n"` is used and gives for example:
```
qdisc fq_codel 0: root refcnt 2 limit 10240p flows 1024 quantum 1514 target 5ms interval 100ms memory_limit 32Mb ecn drop_batch 64  Sent 0 bytes 0 pkt (dropped 0, overlimits 0 requeues 0)  backlog 0b 0p requeues 0  maxpacket 0 drop_overlimit 0 new_flow_count 0 ecn_mark 0  new_flows_len 0 old_flows_len 0
```

## TODO
* Implement statistics on aggregated measurments
* Improve usage simplicity ( file handling )
* Choose between treatment on loading or treatment on csv writing
* Parse csv header to load tare values
* Plot drop and ECN marks in different subplot
* Change "rtr" into "bm" (baremetal) and "rtrvm" into "vm" (Virtual Machine)
* Improve verbose mode if "-v" provided
* Combine raw input file with packet captured to get more stats using `scapy`
* NetTrace: add a specific case for pfifo_fast in plot_all()
* NetTrace: add color consistency in plot_all()
* Add calculation of actual sending rate for endpoints
* Add config file to store infos for data location (input and output files path)
