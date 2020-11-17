# this will run on the designated server pi, along with redis 

import zmq
from time import time, sleep
import sys
import redis
import pickle

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)

redis_db = redis.Redis(host='localhost', port=6379)

print('entering zmq loop')
while True:
    # redis db should look like this:
    # key : '{ 'data' : {dataname1 : data1, dataname2: data2}, 'command' : {commandname1 : command1, commandname2 : command2}, 'time' : time}'   
    # from iot device, I'll recieve pickled { 'key': iotName, 'data': dataDictionary }
    # to iot device, I'll send pickled commandDictionary (no key)
    
    keyAndData = socket.recv()
    # decontruct all info from iot device
    unpickled = pickle.loads(keyAndData)
    key = unpickled['key']      # string
    data = unpickled['data']    # dictionary
    # here I can do things with the data like data['creekLowTime']
    print(data['creekLowTime'])

    sleep(1)
    
    # to be updated later. This time should be structure/entered as above 
    keytime = key + "-time"
    pickledTime = pickle.dumps(time())
    redis_db.set(keytime, pickledTime) 

    # send = { 'lowAg': 'on', 'medAg': 'off' } 
    # get command dictionary
    fullValue = redis_db.get(key)
    unpickledFullValue = pickle.loads(fullValue)
    unpickledCommand = unpickledFullValue['command'] 
    # pickle and send command dictionary
    pickledCommand = pickle.dumps(unpickledCommand)
    socket.send(pickledCommand)

