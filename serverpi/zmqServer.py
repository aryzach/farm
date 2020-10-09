# this will run on the designated server pi, along with redis 

import zmq
import time
import sys
import redis
from time import time, sleep 
import pickle


port = "5556"
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)

redis_db = redis.Redis(host='localhost', port=6379)

print("entering zmq loop")
while True:
    
    
    # this is where the message will be the flow rate / pressure. Really any input sensor from the pi
    # but for now, I'm using it to send the key of which I want to know the value
    key = socket.recv().decode('utf-8')
    keytime = key + "-time"
    pickledTime = pickle.dumps(time())
    redis_db.set(keytime, pickledTime) 
    sleep(1)
    
    value = redis_db.get(key)
    socket.send(value)

