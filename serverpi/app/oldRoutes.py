from twistedApp import app
from flask import render_template, flash, redirect, url_for
from flask_redis import FlaskRedis
from app.forms import PumpForm 
from flask_wtf import FlaskForm
from wtforms import SubmitField
import pickle
from .tools import ping, timeTools

app.config['REDIS_URL'] = "redis://:@localhost:6379/0"
redis_client = FlaskRedis(app)

#initialize database
initialPumpsState = {"lowAg" : "off", "medAg" : "off"}
redis_client.set("creekpi",pickle.dumps(initialPumpsState)) 

@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():
    return render_template('base.html') 

@app.route('/pumps', methods=['GET','POST'])
def pumps():
    form = PumpForm()
    pickled = redis_client.get("creekpi")
    unpickled = pickle.loads(pickled)
    print(unpickled)
    pickledTime = redis_client.get("creekpi-time")
    unpickledTime = pickle.loads(pickledTime)

    lowAgPumpStatus = unpickled['lowAg']
    medAgPumpStatus = unpickled['medAg']

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
    unpickled[pump] = status
    print(unpickled)
    pickled = pickle.dumps(unpickled)
    redis_client.set('creekpi',pickled)


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

