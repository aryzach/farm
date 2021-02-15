import paho.mqtt.publish as publish
import redis
import pickle


redis_db = redis.Redis(host='localhost', port=6379)

while True:
    pickled = redis_db.get('valves')
    unpickled = pickle.loads(pickled)
    command = unpickled['command']
    for key, value in command.items():
        if value == 'on':
            publish.single(key, "1", hostname='localhost')
        else:
            publish.single(key, "0", hostname='localhost')
