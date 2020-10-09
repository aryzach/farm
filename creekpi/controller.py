import RPi.GPIO as GPIO
import time
from gpiozero import Button

GPIO.setmode(GPIO.BCM)

# init list with pin numbers

outpins = [14,15]
inpins = [2] 

lowAgPin = 14
medAgPin = 15

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
    return not floatSwitch.is_pressed

def lowAgOff():
    pumpOff(lowAgPin)

def medAgOff():
    pumpOff(medAgPin)

def cycleLowAg():
    cyclePump(lowAgPin)

def cycleMedAg():
    cyclePump(medAgPin)

