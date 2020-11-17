from flask_redis import FlaskRedis
import pickle
from flask import Flask
from flask_redis import FlaskRedis

app = Flask(__name__)
redis_client = FlaskRedis(app)

#app.config['REDIS_URL'] = "redis://:@localhost:6379/0"
#redis_client = FlaskRedis(app)

#initialize database creekpi
# TODO: redis.get(creekpi), if no value, then set all. If value exists, set only initial pump states and maybe others
key = 'creekpi'
commandDictionary = {"lowAg" : "off", "medAg" : "off"}
dataDictionary = {}
fullValue = {'data' : dataDictionary, 'command' : commandDictionary}
pickledFullValue = pickle.dumps(fullValue)
redis_client.set(key,pickledFullValue)


