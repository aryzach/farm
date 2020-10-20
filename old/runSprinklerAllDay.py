from flask import Flask, render_template, request, send_from_directory, jsonify
from flask_redis import FlaskRedis
import sys
import re
import pickle
import json
import datetime
import time

sys.path.append('../vehicle')


app = Flask(__name__) 
app.config['REDIS_URL'] = "redis://:@localhost:6379/0"
redis_client = FlaskRedis(app)

while True:
    redis_client.set('waterTankToNE', 'closed')
    time.sleep(60*60*2)
    redis_client.set('waterTankToNE', 'open')
    time.sleep(60*60)


