import matplotlib.pyplot as plt 
import numpy as np 
from matplotlib.colors import LogNorm 
import json
import ast


jlines = []
times = []

with open('ping.txt','r') as f:
    #lines = f.read().splitlines()
    for line in f:
        if line[0] == '{':
            jlines.append(ast.literal_eval(json.loads(json.dumps(line.strip()))))
        else:
            times.append(line.strip())
    f.close()

times = times[1::2]

devices = list(map(lambda x: list(x.keys()), jlines))[0]

latencies = list(map(lambda x: list(x.values()), jlines))



     
plt.pcolormesh(latencies, cmap='Reds') 
  
plt.xticks(list(range(len(devices))),devices,rotation='vertical')
plt.yticks(list(map(lambda x:x*2,list(range(len(times))))), times, rotation='horizontal',size='x-small')
plt.colorbar()
plt.show() 
