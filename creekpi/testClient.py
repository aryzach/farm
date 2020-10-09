import zmq 
import sys 
import time
import controller 
import pickle

# IP where zmqServer.py is running
serverIP = "192.168.1.123"
port = "5556"
serverDestination = serverIP + ":" + port 
fullDestination = "tcp://" + serverDestination

#context = zmq.Context()
#print("Connecting to server...")
#socket = context.socket(zmq.REQ)
#socket.connect(fullDestination)

def sending(socket):
    try:
        socket.send_string("creekpi")
    except zmq.error.Again as e:
        print("Remote server unreachable.")
        timeout_milliseconds = 100

def recieving(socket):
    print("Poll socket.")
    print(socket.poll(timeout=1000))
    while socket.poll(timeout=1000):
        print("reading socket.")
        pickled = socket.recv()
        unpickled = pickle.loads(pickled)
        return socket, True, unpickled 
    return socket, False, "nothing"

def initialConnection(connected):
    while not connected:
        context = zmq.Context()
        print("creating socket")
        socket = context.socket(zmq.REQ)
        socket.connect(fullDestination)
        sending(socket)
        socket, connected, nothing = recieving(socket)
        if not connected:
            print("destroy")
            context.destroy(linger=0)
            print("destroyed")
    return socket

def control(lowAgCommand,medAgCommand):
    if lowAgCommand == "on":
        controller.cycleLowAg()

    elif lowAgCommand == "off":
        controller.lowAgOff()

    if medAgCommand == "on":
        controller.cycleMedAg()

    elif medAgCommand == "off":
        controller.medAgOff()
        

def mainLoop(socket):
    print("entering loop")
    while True:
        # instead of sending valve position, this is where I'll send flow rate / pressure from the pi
        # for now I'm sending the key that I want o know the value o
    
       sending(socket)
       socket, connected, unpickled = recieving(socket)

       control(unpickled['lowAg'], unpickled['medAg'])

mainLoop(initialConnection(False)) 
