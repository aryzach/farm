import RPi.GPIO as GPIO
import time
import sys
import redis

GPIO.setmode(GPIO.BCM)

# init list with pin numbers

pinList = [2, 3, 4, 
           17, 27, 22, 
           10, 9, 11, 
           5, 6, 13, 
           19, 26, 21, 20]

activatingPins = [4, 22, 6, 26]
RELAY1 = 4
RELAY2 = 22
RELAY3 = 6
RELAY4 = 26

# loop through pins and set mode and state to 'low'

for i in pinList:
  GPIO.setup(i, GPIO.OUT)
  GPIO.output(i, GPIO.LOW)

# time to sleep between operations in the main loop

SleepTimeL = 15 

# main loop

def closeValve():  
  GPIO.output(RELAY1, GPIO.HIGH)
  GPIO.output(RELAY3, GPIO.HIGH)
  time.sleep(SleepTimeL)
  GPIO.output(RELAY1, GPIO.LOW)
  GPIO.output(RELAY3, GPIO.LOW)
  print("valve is closed")

def openValve():  
  GPIO.output(RELAY2, GPIO.HIGH)
  GPIO.output(RELAY4, GPIO.HIGH)
  time.sleep(SleepTimeL)
  GPIO.output(RELAY2, GPIO.LOW)
  GPIO.output(RELAY4, GPIO.LOW)
  print("valve is open") 

# test function to determine relay pins
def relay(a):
  print (a)
  GPIO.output(a, GPIO.HIGH)
  time.sleep(SleepTimeL)
  GPIO.output(a, GPIO.LOW)
  time.sleep(SleepTimeL)
  print (a)


if len(sys.argv) == 2:
  command = sys.argv[1]
  if command == "close":
      closeValve()
  elif command == "open":
      openValve()

