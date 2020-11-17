import sys
import zmq
import time

port = "1883"
context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.bind("tcp://*:%s" % port)

while True:
    message= socket.recv()
    print(message)
