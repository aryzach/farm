import zmq 
import sys 
import time
import testclasscontroller 
import pickle
from datetime import datetime

REQUEST_TIMEOUT = 2500


# IP where zmqServer.py is running
serverIP = "localhost"
port = "5556"
serverDestination = serverIP + ":" + port 
SERVER_ENDPOINT = "tcp://" + serverDestination

context = zmq.Context()
print("Connecting to server...")
client = context.socket(zmq.REQ)
client.connect(SERVER_ENDPOINT)

creekLogger = testclasscontroller.CreekLogger()

def control(lowAgCommand,medAgCommand):
    if lowAgCommand == "on":
        print('low on') 

    elif lowAgCommand == "off":
        print('low off')

    if medAgCommand == "on":
        print('med on')

    elif medAgCommand == "off":
        print('med off')
        
while True:
    if creekLogger.decideCreekLowLog():
        creekLowTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    else:
        creekLowTime = None
    keyAndData = { 'key': 'creekpi', 'data': {'creekLowTime': creekLowTime} }
    pickledKeyAndData = pickle.dumps(keyAndData)
    client.send(pickledKeyAndData)

    # part of zmq lazy pirate pattern
    while True:
        if (client.poll(REQUEST_TIMEOUT) & zmq.POLLIN) != 0:
            pickledCommandDictionary = client.recv()
            unpickledCommandDictionary = pickle.loads(pickledCommandDictionary)
            control(unpickledCommandDictionary['lowAg'], unpickledCommandDictionary['medAg'])
            break

        # Socket is confused. Close and remove it.
        client.setsockopt(zmq.LINGER, 0)
        client.close()

        # Create new connection
        client = context.socket(zmq.REQ)
        print("Reconnecting to server")
        client.connect(SERVER_ENDPOINT)
        client.send(pickledKeyAndData)


    
