from app import app
from flask import render_template, flash, redirect, url_for
from flask_redis import FlaskRedis
from app.forms import LowAgForm 
from flask_wtf import FlaskForm
from wtforms import SubmitField

app.config['REDIS_URL'] = "redis://:@localhost:6379/0"
redis_client = FlaskRedis(app)

@app.route('/')
@app.route('/index')
def index():
    return "hi" 

@app.route('/lowAg', methods=['GET','POST'])
def lowAg():
    form = LowAgForm()
    pos = redis_client.get('waterTankToNE').decode()
    print(pos)

    if form.validate_on_submit():
        if form.on.data:
            print('on')
            redis_client.set('waterTankToNE','open') 
            return redirect(url_for('lowAg'))
        elif form.off.data:
            print('off')
            redis_client.set('waterTankToNE','closed')
            return redirect(url_for('lowAg'))

    return render_template('lowAg.html', form=form, pos=pos)

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


