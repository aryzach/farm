import RPi.GPIO as GPIO
import time
from gpiozero import Button
from datetime import datetime

GPIO.setmode(GPIO.BCM)

# init list with pin numbers

outpins = [14,15]
inpins = [2] 

lowAgPin = 14
medAgPin = 15

floatSwitch = Button(2) 

# global vars!
wasCreekLow = False

# loop through pins and set mode and state to 'low'

for i in outpins:
    GPIO.setup(i,GPIO.OUT)
    GPIO.output(i,GPIO.LOW)

for i in inpins:
    GPIO.setup(i,GPIO.IN)

def pumpOn(pump):  
  GPIO.output(pump, GPIO.HIGH)

def pumpOff(pump):  
  GPIO.output(pump, GPIO.LOW)

def cyclePump(pump):
    if isCreekLow():
        pumpOff(pump)
    else:
        pumpOn(pump)
    
def isCreekLow():
    isCreekLow = not floatSwitch.is_pressed
    decideCreekLowLog(isCreekLow)
    return isCreekLow 

def decideCreekLowLog(isCreekLow):
    if isCreekLow and not wasCreekLow:
        writeTime()
        wasCreekLow = True
    elif not isCreekLow:
        wasCreekLow = False

def writeTime():
    outFile = open("creekOff.txt", "a")
    outFile.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    outFile.close()
    
def lowAgOff():
    pumpOff(lowAgPin)

def medAgOff():
    pumpOff(medAgPin)

def cycleLowAg():
    cyclePump(lowAgPin)

def cycleMedAg():
    cyclePump(medAgPin)

