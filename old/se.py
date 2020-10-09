from random import randint
import itertools
import logging
import time
import zmq

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)

context = zmq.Context()
server = context.socket(zmq.REP)
server.bind("tcp://*:5555")

for cycles in itertools.count():
    request = server.recv()


    logging.info("Normal request (%s)", request)
    time.sleep(1)  # Do some heavy work
    server.send(request)
