# this will run on the designated server pi, along with redis 

import zmq
import time
import sys
import redis

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)

redis_db = redis.Redis(host='localhost', port=6379)

while True:
    
    # this is where the message will be the flow rate / pressure. Really any input sensor from the pi
    message = socket.recv().decode("utf-8")

    print ("valve position is: ", message)

    time.sleep(1)
    valveDbValue = redis_db.get("waterTankToNE").decode("utf-8")
    print ("valveDbValue is: ", valveDbValue)
    socket.send_string(valveDbValue)
