import RPi.GPIO as GPIO
import time
from gpiozero import Button
from datetime import datetime

GPIO.setmode(GPIO.BCM)

# init list with pin numbers

outpins = [14,15,20,21]
inpins = [2] 

lowAgPin = 14
medAgPin = 15
highAgPin = 20
domPin = 21

floatSwitch = Button(2) 


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
    return isCreekLow 

class CreekLogger:
    def __init__(self):
        self.wasCreekLow = False 

    def decideCreekLowLog(self):
        if isCreekLow() and not self.wasCreekLow:
            self.wasCreekLow = True
            return True
        elif not isCreekLow():
            self.wasCreekLow = False
            return False
        else:
            return False


def writeTime():
    outFile = open("creekOff.txt", "a")
    outFile.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    outFile.close()
    
def lowAgOff():
    pumpOff(lowAgPin)

def medAgOff():
    pumpOff(medAgPin)

def highAgOff():
    pumpOff(highAgPin)

def domOff():
    pumpOff(domPin)


def cycleLowAg():
    cyclePump(lowAgPin)

def cycleMedAg():
    cyclePump(medAgPin)

def cycleHighAg():
    cyclePump(highAgPin)

def cycleDom():
    cyclePump(domPin)

