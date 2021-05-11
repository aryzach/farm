import zmq 
import sys 
import time
import controller 
import pickle
from datetime import datetime

REQUEST_TIMEOUT = 2500


# IP where zmqServer.py is running
serverIP = "192.168.1.7"
port = "5556"
serverDestination = serverIP + ":" + port 
SERVER_ENDPOINT = "tcp://" + serverDestination

context = zmq.Context()
print("Connecting to server...")
client = context.socket(zmq.REQ)
client.connect(SERVER_ENDPOINT)

creekLogger = controller.CreekLogger()

def control(lowAgCommand,medAgCommand,highAgCommand,domCommand):
    if lowAgCommand == "on":
        controller.cycleLowAg()

    elif lowAgCommand == "off":
        controller.lowAgOff()

    if medAgCommand == "on":
        controller.cycleMedAg()

    elif medAgCommand == "off":
        controller.medAgOff()

    if highAgCommand == "on":
        controller.cycleHighAg()

    elif highAgCommand == "off":
        controller.highAgOff()

    if domCommand == "on":
        controller.cycleDom()

    elif domCommand == "off":
        controller.domOff()
        
while True:
    if creekLogger.decideCreekLowLog():
        creekLowTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    else:
        creekLowTime = None
    keyAndData = { 'key': 'creekpi', 'data': {'creekLowTime': creekLowTime} }
    pickledKeyAndData = pickle.dumps(keyAndData)
    client.send(pickledKeyAndData)

    while True:
        if (client.poll(REQUEST_TIMEOUT) & zmq.POLLIN) != 0:
            pickledCommandDictionary = client.recv()
            unpickledCommandDictionary = pickle.loads(pickledCommandDictionary)
            control(unpickledCommandDictionary['lowAg'], unpickledCommandDictionary['medAg'],unpickledCommandDictionary['highAg'],unpickledCommandDictionary['dom'])
            break

        # Socket is confused. Close and remove it.
        client.setsockopt(zmq.LINGER, 0)
        client.close()

        # Create new connection
        client = context.socket(zmq.REQ)
        print("Reconnecting to server")
        client.connect(SERVER_ENDPOINT)
        client.send(pickledKeyAndData)


    
