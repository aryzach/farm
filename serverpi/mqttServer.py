import paho.mqtt.publish as publish
import redis
import pickle
import time
import json

SLEEP = 6

redis_db = redis.Redis(host='localhost', port=6379)

print("starting MQTT server")
'''
while True:
    test = { "p00d00" : "on", "p00d01" : "on" }
    data = json.dumps(test)
    print(data)
    publish.single("valves",data, hostname='localhost')
    time.sleep(SLEEP)
    test = { "p00d00" : "off", "p00d01" : "off" }
    data = json.dumps(test)
    print(data)
    publish.single("valves",data, hostname='localhost')
    time.sleep(SLEEP)
'''
while True:
        pickled = redis_db.get('valves')
        unpickled = pickle.loads(pickled)
        commandTupleList = unpickled['command']
        data = json.dumps(commandTupleList)
        publish.single("valves",data, hostname='localhost')
        print(data)
        time.sleep(SLEEP)
