import zmq 
import sys 
import time
import controller as c 
import pickle
from datetime import datetime

REQUEST_TIMEOUT = 2500


# IP where zmqServer.py is running
serverIP = "192.168.1.123"
port = "5556"
serverDestination = serverIP + ":" + port 
SERVER_ENDPOINT = "tcp://" + serverDestination

context = zmq.Context()
print("Connecting to server...")
client = context.socket(zmq.REQ)
client.connect(SERVER_ENDPOINT)

while True:
    keyAndData = { 'key': 'cooppi', 'data': {'ID': c.read()} }
    pickledKeyAndData = pickle.dumps(keyAndData)
    client.send(pickledKeyAndData)

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


    
