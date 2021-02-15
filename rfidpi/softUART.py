import sys
import time
import difflib
import pigpio

 
RX=19
BAUDRATE = 9600 
BITS = 8
SLEEP = .2

pi = pigpio.pi()

prevID = 0

# open a gpio to bit bang read the echoed data (soft RX pin)
try:
    pi.bb_serial_read_open(RX, BAUDRATE, BITS)
except:
    pi.bb_serial_read_close(RX)
    pi.bb_serial_read_open(RX, BAUDRATE, BITS)

def handleID(data):
    ID = (data.decode('utf-8'))
    #print(ID[0].encode())
    if ID[0].encode() == b'\x02':
        ID = ID[3:11]
        ID = int(ID,16)
        epoch = int(time.time())
        text = f'{epoch}:{ID}\n'
        global prevID
        if prevID != ID:
            prevID = ID
            with open("softUART.txt", "a") as myfile:
                myfile.write(text)

while True:
    (count, data) = pi.bb_serial_read(RX)
    if data:
        try:
            handleID(data)
        except:
            pass
    time.sleep(SLEEP)


