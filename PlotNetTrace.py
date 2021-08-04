#!/usr/bin/env python3
import sys
from pathlib import Path
from matplotlib import pyplot as plt
import numpy as np
from Plot import *


args   = list(sys.argv)
ipath  = 'data/'
opath  = 'output/'
suffix = ["rtr","atk","cc","lc","cs","ls","rtrvm"]

date                = ""
timecode            = ""
files               = {}
files["rtr_file"]   = None 
files["atk_file"]   = None
files["cc_file"]    = None
files["lc_file"]    = None
files["cs_file"]    = None
files["ls_file"]    = None
files["rtrvm_file"] = None

verbose_mode  = False
timecode_mode = False
timefreq_mode = False
special_mode  = False
rewrite_mode  = False
multiexp_mode = False

for arg in sys.argv:
    if arg in ["verbose","-v","timecode", "rewrite", "timefreq", "special", "multiexp"]:
        args.remove(arg)
        if arg in ["verbose","-v"]:
            verbose_mode=True
        elif arg == "timecode":
            timecode_mode=True
        elif arg == "timefreq":
            timefreq_mode=True
        elif arg == "special":
            special_mode=True
        elif arg == "multiexp":
            multiexp_mode=True
        elif arg == "rewrite":
            rewrite_mode=True


if timecode_mode is True and len(args) == 3:
    date = args[1]
    timecode = args[2]
    dirpath = ipath + date + "/" + timecode

    for node in suffix:
        filename = dirpath+"-"+node
        node_exist = Path(filename).is_file()
        
        if verbose_mode is True:
            files[node+"_file"] = filename if node_exist is True else print("Info: file {} does not exist.".format(filename))
        else:
            if node_exist is True: files[node+"_file"] = filename
    
elif timecode_mode is False and len(args) in range(2,8) and multiexp_mode is not True:
    if Path(args[-1]).is_file() is not True:
        sys.exit(f"File {args[-1]} does not exists")

    date =  args[-1].split("/")[-2]
    timecode = args[-1].split("/")[-1].split("-")[-2]
    
    for f in args:
        file_exist = Path(f).is_file()
        if file_exist is not True:
            sys.exit(f"File {f} does not exists")

        for node in suffix:
            if f.split("-")[-1] == node:
                files[node+"_file"] = f
                if verbose_mode is True:
                    print("Info: Loading file {}.".format(f))
elif multiexp_mode is True and len(args) == 2:
    exp_path = ipath+args[-1]+"/"

else:
    sys.exit("Invalid arguments. Expected usage:\n"+str(args[0])+" rtr_file atk_file cc_file lc_file cs_file ls_file\nor\n"+str(args[0])+" timecode 2021-05-20 1516\n")
    


PlotNetTrace = Plot(date, timecode, files["rtr_file"], files["atk_file"], files["cc_file"], files["lc_file"], files["cs_file"], files["ls_file"], files["rtrvm_file"], rewrite_mode)
if special_mode is True:
    PlotNetTrace.special_plot()
elif timefreq_mode is True:
    PlotNetTrace.timefreq_plot()
elif multiexp_mode is True:
    PlotNetTrace.multiexp_plot(exp_path)
else:
    PlotNetTrace.visualize()


