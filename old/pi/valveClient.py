import zmq
import sys
import time
import valveController as VC

# IP where zmqServer.py is running
serverIP = "192.168.1.123"
port = "5556"
serverDestination = serverIP + ":" + port 
fullDestination = "tcp://" + serverDestination


context = zmq.Context()
print("Connecting to server...")
socket = context.socket(zmq.REQ)
socket.connect(fullDestination)
#socket.connect("tcp://192.168.1.207:%s" % port)

valvePosition = "closed" 

print("entering loop")
while True:
    # instead of sending valve position, this is where I'll send flow rate / pressure from the pi
    socket.send_string(valvePosition)

    # the message value is what I'll use to open or close the valve
    message = socket.recv().decode("utf-8")

    if message != valvePosition:
        valvePosition = message
        if message == "open":
            VC.openValve()
        elif message == "closed":
            VC.closeValve()
        print("valve is changing to ", message)

