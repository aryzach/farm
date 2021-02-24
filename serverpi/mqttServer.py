import paho.mqtt.publish as publish
import redis
import pickle
import time

SLEEP = 2

redis_db = redis.Redis(host='localhost', port=6379)

print("starting MQTT server")

while True:
        pickled = redis_db.get('valves')
        unpickled = pickle.loads(pickled)
        commandTupleList = unpickled['command']
        for valveTpl in commandTupleList:
            valve = valveTpl[0]
            state = valveTpl[1]
            if state == 'on':
                publish.single(valve, "1", hostname='localhost')
            else:
                publish.single(valve, "0", hostname='localhost')
        time.sleep(SLEEP)
