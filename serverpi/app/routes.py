from twistedApp import app
from flask import render_template, flash, redirect, url_for, send_file
from flask_redis import FlaskRedis
from app.forms import PumpForm 
from flask_wtf import FlaskForm
from wtforms import SubmitField
import pickle
from .tools import ping, timeTools

import matplotlib.pyplot as plt 
import numpy as np 
from matplotlib.colors import LogNorm 
import json
import ast
import io 


app.config['REDIS_URL'] = "redis://:@localhost:6379/0"
redis_client = FlaskRedis(app)

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
    unpickledTime = pickle.loads(pickledTime)

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

    print(ping.getPing("creekpi"))
    if ping.getPing("creekpi") and timeTools.isRecent(unpickledTime):
        return render_template('pumps.html', form=form, lowAgPumpStatus=lowAgPumpStatus, medAgPumpStatus=medAgPumpStatus)
    else:
        return render_template('notAvailable.html')


def setPumps(unpickled, pump, status):
    data = unpickled['data']
    command = unpickled['command']  # dictionary
    command[pump] = status
    unpickled['command'] = command
    pickled = pickle.dumps(unpickled)
    redis_client.set('creekpi',pickled)

@app.route('/network', methods=['GET'])
def network():
    fig = generatePlot() 
    img = io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')
    
    #canvas = FigureCanvas(fig)
    #output = io.BytesIO() 
    #canvas.print_png(output)
    #response = make_response(output.getvalue())
    #response.mimetype = 'image/png'
    #return response

    #return render_template("network.html", plot = '/home/pi/twistedApp/static/images/new_plot.png')
    #return render_template('network.html', name = 'new_plot', url ='/home/pi/twistedApp/static/images/new_plot.png')

def generatePlot():
    timeSpacing = 4
    jlines = []
    times = []
    with open('/home/pi/twistedApp/app/tools/network/ping.json','r') as f:
     #lines = f.read().splitlines()
        for line in f:
            if line[0] == '{':
                jlines.append(ast.literal_eval(json.loads(json.dumps(line.strip()))))
            else:
                times.append(line.strip())
        f.close()

    times = times[1::timeSpacing]
    devices = list(map(lambda x: list(x.keys()), jlines))[0]
    latencies = list(map(lambda x: list(x.values()), jlines))

    plt.figure(figsize=(21,11),tight_layout=True)  
    plt.pcolormesh(latencies, cmap='Reds') 
    plt.xticks(list(range(len(devices))),devices,rotation='vertical',size='small')
    plt.yticks(list(map(lambda x:x*timeSpacing,list(range(len(times))))), times, rotation='horizontal',size='small')
    plt.colorbar()
    plt.savefig('/home/pi/twistedApp/static/images/new_plot.jpg')

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

