import time
import serial
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
 
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
GPIO.output(23,False)
GPIO.output(24,False)
PortRF = serial.Serial("/dev/ttyS0",baudrate=9600,timeout=0.2)

def getID():    
    for Counter in range(12):
        read_byte=PortRF.read()
        ID = ID + read_byte.decode('utf-8')
        ID = int(ID[2:10],16)
    return str(ID)

def read():
    read_byte = PortRF.read()
    if read_byte == b'\x02':
        return getID()
    else:
        return "" 

    
    

