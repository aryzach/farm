import matplotlib.pyplot as plt 
import numpy as np 
from matplotlib.colors import LogNorm 
import json



def generatePlot():
    TIMESPACING = 4
    TIMEPOINTS = 100

    with open('ping.json','r') as f:
        jlines = json.load(f)

    times = (list(jlines.keys()))[-TIMEPOINTS:]
    
    showTimes = times[1::TIMESPACING]

    destinations = list(jlines[times[-1]].keys())
    print(len(destinations))
    print(destinations)

    latencies = list(map(lambda x: list((jlines[x]).values()), jlines))[-TIMEPOINTS:]
    print(len(latencies[0]))

    plt.figure(figsize=(21,11),tight_layout=True)  
    plt.pcolormesh(latencies, cmap='Reds') 
    plt.xticks(list(range(len(destinations))),destinations,rotation='vertical',size='small')
    plt.yticks(list(map(lambda x:x*TIMESPACING,list(range(len(showTimes))))), showTimes, rotation='horizontal',size='small')
    plt.colorbar()

    plt.show() 


generatePlot()
