# this is a test client. Similar code will run on the pi

import zmq
import sys
import time

valvePosition = "open"

port = "5556"

context = zmq.Context()
print("Connecting to server...")
socket = context.socket(zmq.REQ)
socket.connect ("tcp://localhost:%s" % port)

while True:
    # instead of sending valve position, this is where I'll send flow rate / pressure from the pi
    socket.send_string(valvePosition)

    # the message value is what I'll use to open or close the valve
    message = socket.recv().decode("utf-8")

    if message == valvePosition:
        print("not changed ", message)
    else:
        valvePosition = message
        print("valve is changing to ", message)

    time.sleep(1)
