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

## Requirements

* python3
* `matplotlib`
* `numpy`
* `parse`

## TODO
* Usage:        Improve usage simplicity ( file handling )
* Usage:        Improve verbose mode if "-v" provided
* Usage:        Provide better documentation and usage message
* Usage:        Add config file to store infos for data location (input and output files path)
* Data Loading: Do all data treatment on loading  (no treatments on csv writing)
* CSV Header:   Check if more tare value are needed (in order to parse csv header to load tare values)
* CSV Header:   Retrieve packet limits configuration value in csv header to calculate queue occupation ratio (currently hardcoded with default value)
* CSV Header:   Retrieve max rate configuration value in csv header to calculate link utilization (instant Mbps / max_rate)
* NetTrace.py:  Create a class router and a class endpoint that both implements attributes of Measure class
* NetTrace.py:  Change add_matched_field() to not return ','
* NetTrace.py:  Synchronize measurments (provide a common timestamp when writing raw data ?)
* NetTrace.py:  Correct Data rate artefacts + loop problem ( above max of bytes_acked value in ss, it seems to overflow and it goes back to 0 )
* Change "rtr" into "bm" (baremetal) and "rtrvm" into "vm" (Virtual Machine)
* Combine raw input file with packet captured to get more stats using `scapy`
* Check calculation of data_rate() for endpoints
* Start to dev detection tools
* Implement statistics on aggregated measurments
* Improve histogram by centering and reducing data
