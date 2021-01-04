from flask_redis import FlaskRedis
import matplotlib.pyplot as plt 
import numpy as np 
from matplotlib.colors import LogNorm 
from pathlib import Path
import time
import pickle
from datetime import datetime
import pytz
import os

#app.config['REDIS_URL'] = "redis://:@localhost:6379/0"
#redis_client = FlaskRedis(app)


def getData():
    return pickle.loads(redis_client.get('cooppi'))['data'] # { ID : [times] }

def getSimpleTimeOfToday(military):
    utc_now = pytz.utc.localize(datetime.utcnow())
    d = utc_now.astimezone(pytz.timezone("America/Los_Angeles")).strftime("%Y-%m-%d")
    d = d + ' {0}:00:00'.format(military)
    p = '%Y-%m-%d %H:%M:%S'
    epoch = int(time.mktime(time.strptime(d,p)))
    return epoch

def generateChickenPlot():
    data = getData()



    TIMESPACING = 4
    TIMEPOINTS = 100


    times = (list(jlines.keys()))[-TIMEPOINTS:]
    showTimes = times[1::TIMESPACING]

    destinations = list(jlines[times[-1]].keys())

    latencies = list(map(lambda x: list((jlines[x]).values()), jlines))[-TIMEPOINTS:]

    fig = plt.figure(figsize=(21,11),tight_layout=True)  
    ax = fig.add_subplot(111) #
    plt.pcolormesh(latencies, cmap='Reds',linewidth=5)
    ax.grid(True, color="crimson", lw=2,axis='x') 
    plt.xticks(list(range(len(destinations))),destinations,rotation='vertical',size='small')
    plt.yticks(list(map(lambda x:x*TIMESPACING,list(range(len(showTimes))))), showTimes, rotation='horizontal',size='small')
    plt.colorbar()
    return plt


