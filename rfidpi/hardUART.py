import time
import serial
import RPi.GPIO as GPIO

SLEEP = .2

GPIO.setmode(GPIO.BCM)
 
PortRF = serial.Serial("/dev/ttyS0",baudrate=9600,timeout=0.2)

prevID = 0 

def handleID():    
    ID = ""
    for Counter in range(12):
        read_byte=PortRF.read()
        ID = ID + read_byte.decode('utf-8')
    ID = int(ID[2:10],16)
    epoch = int(time.time())
    text = f'{epoch}:{ID}\n'
    global prevID
    if prevID != ID:
        prevID = ID
        with open("hardUART.txt", "a") as myfile:
            myfile.write(text)


while True:
    read_byte = PortRF.read()
    if read_byte == b'\x02':
        try:
            handleID()
        except:
            pass
    time.sleep(SLEEP)

    

