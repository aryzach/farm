from twistedApp import app
from flask import render_template, flash, redirect, url_for, send_file
from flask_redis import FlaskRedis
from app.forms import PumpForm 
from flask_wtf import FlaskForm
from wtforms import SubmitField
import pickle
from .tools import ping, timeTools
import os
from collections import OrderedDict


import matplotlib.pyplot as plt 
import numpy as np 
from matplotlib.colors import LogNorm 
import json
import ast
import io 
from pathlib import Path
from time import time

app.config['REDIS_URL'] = "redis://:@localhost:6379/0"
redis_client = FlaskRedis(app)

PINGFILE = os.path.join(os.path.dirname(__file__), 'tools/network/ping.json')
TESTSPEEDFILE = os.path.join(os.path.dirname(__file__), 'tools/network/testspeed.json')



#initialize database creekpi
# TODO: redis.get(creekpi), if no value, then set all. If value exists, set only initial pump states and maybe others
key = 'creekpi'
commandDictionary = {"lowAg" : "off", "medAg" : "off"}
dataDictionary = {}
fullValue = {'data' : dataDictionary, 'command' : commandDictionary}
pickledFullValue = pickle.dumps(fullValue)
redis_client.set(key,pickledFullValue)

@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():
    return render_template('base.html') 

@app.route('/pumps', methods=['GET','POST'])
def pumps():
    form = PumpForm()
    pickled = redis_client.get("creekpi")
    # redis db should look like this:
    # key : '{ 'data' : {dataname1 : data1, dataname2: data2}, 'command' : {commandname1 : command1, commandname2 : command2}, 'time' : time}'
    unpickled = pickle.loads(pickled)   # dictionary
    command = unpickled['command']
    data = unpickled['data']
    pickledTime = redis_client.get("creekpi-time")
    if pickledTime == None:
        timeIsRecent = False
    else:
        unpickledTime = pickle.loads(pickledTime)
        timeIsRecent = timeTools.isRecent(unpickledTime)


    lowAgPumpStatus = command['lowAg']
    medAgPumpStatus = command['medAg']

    if form.validate_on_submit():
        if form.onLowAg.data:
            setPumps(unpickled, 'lowAg', 'on')
            return redirect(url_for('pumps'))
        elif form.offLowAg.data:
            setPumps(unpickled, 'lowAg', 'off')
            return redirect(url_for('pumps'))
        elif form.onMedAg.data:
            setPumps(unpickled, 'medAg', 'on')
            return redirect(url_for('pumps'))
        elif form.offMedAg.data:
            setPumps(unpickled, 'medAg', 'off')
            return redirect(url_for('pumps'))

    #print(ping.getPing("creekpi"))
    if ping.getPing("creekpi") and timeIsRecent:
        return render_template('pumps.html', form=form, lowAgPumpStatus=lowAgPumpStatus, medAgPumpStatus=medAgPumpStatus)
    else:
        return render_template('notAvailable.html', device='tom, creek thing')


def setPumps(unpickled, pump, status):
    data = unpickled['data']
    command = unpickled['command']  # dictionary
    command[pump] = status
    unpickled['command'] = command
    pickled = pickle.dumps(unpickled)
    redis_client.set('creekpi',pickled)

@app.route('/network', methods=['GET'])
def network():
    if Path(PINGFILE).exists():
        fig = generatePingPlot() 
        img = io.BytesIO()
        fig.savefig(img)
        img.seek(0)
        return send_file(img, mimetype='image/png')
    else:
        return render_template('notAvailable.html', device='network tool')

    

def generatePingPlot():
    TIMESPACING = 4
    TIMEPOINTS = 100

    with open(PINGFILE,'r') as f:
        allInfo = json.load(f)

    sortedAllInfo = OrderedDict(sorted(allInfo.items(),reverse=True))

    #times = (list(jlines.keys()))[-TIMEPOINTS:]
    times = (list(sortedAllInfo.keys()))
    showTimes = times[1::TIMESPACING]

    #sortedDestinations = list(jlines[times[-1]].keys()).sort()
    #destinations = list(jlines[times[-1]].keys())
    #for each time segment, this is the results dict where each is unsorted 
    resultsDicts = list(sortedAllInfo.values())

    #now each of those is sorted by destination (all are OrderDicts)
    sortedResultsDicts = list(map(lambda x: OrderedDict(sorted(x.items())), resultsDicts))

    #sorted destinations from most recent results
    destinations = list(list(map(lambda x: x.keys(),sortedResultsDicts))[-1])
    latencies = list(list(map(lambda x: list(x.values()),sortedResultsDicts)))

    #latencies = list(map(lambda x: list((jlines[x]).values()), jlines))[-TIMEPOINTS:]
    #latencies = list(map(lambda x: list((OrderedDict(sorted(jlines[x].items()))).values()), jlines))[-TIMEPOINTS:]

    fig = plt.figure(figsize=(21,11),tight_layout=True)  
    ax = fig.add_subplot(111) #
    plt.pcolormesh(latencies, cmap='Reds',linewidth=5)
    ax.grid(True, color="crimson", lw=2,axis='x') 
    plt.xticks(list(range(len(destinations))),destinations,rotation='vertical',size='small')
    plt.yticks(list(map(lambda x:x*TIMESPACING,list(range(len(showTimes))))), showTimes, rotation='horizontal',size='small')
    plt.colorbar()
    return plt


@app.route('/testspeed', methods=['GET'])
def testspeed():
    if Path(TESTSPEEDFILE).exists():
        fig = generateSpeedPlot() 
        img = io.BytesIO()
        fig.savefig(img)
        img.seek(0)
        return send_file(img, mimetype='image/png')
    else:
        return render_template('notAvailable.html', device='speed test tool')

def generateSpeedPlot():
    TIMESPACING = 4
    TIMEPOINTS = 100

    with open(TESTSPEEDFILE,'r') as f:
        jlines = json.load(f)

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



'''
@app.route('/on', methods=['GET'])
def on():
    print("on")
    redis_client.set('waterTankToNE','open') 
    return redirect(url_for('lowAg'))

@app.route('/off', methods=['GET'])
def off():
    print("off")
    redis_client.set('waterTankToNE','closed') 
    return redirect(url_for('lowAg'))
'''

