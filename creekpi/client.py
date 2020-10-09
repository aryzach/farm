import zmq 
import sys 
import time
import controller 
import pickle

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

def control(lowAgCommand,medAgCommand):
    if lowAgCommand == "on":
        controller.cycleLowAg()

    elif lowAgCommand == "off":
        controller.lowAgOff()

    if medAgCommand == "on":
        controller.cycleMedAg()

    elif medAgCommand == "off":
        controller.medAgOff()
        
while True:
    request = "creekpi"
    client.send_string(request)

    while True:
        if (client.poll(REQUEST_TIMEOUT) & zmq.POLLIN) != 0:
            pickled = client.recv()
            unpickled = pickle.loads(pickled)
            control(unpickled['lowAg'], unpickled['medAg'])
            break

        # Socket is confused. Close and remove it.
        client.setsockopt(zmq.LINGER, 0)
        client.close()

        # Create new connection
        client = context.socket(zmq.REQ)
        print("Reconnecting to server")
        client.connect(SERVER_ENDPOINT)
        client.send_string(request)


    
