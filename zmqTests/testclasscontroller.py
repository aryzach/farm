import time
from datetime import datetime


# init list with pin numbers

outpins = [14,15]
inpins = [2] 

lowAgPin = 14
medAgPin = 15


# loop through pins and set mode and state to 'low'

class CreekLogger:
    def __init__(self):
        self.wasCreekLow = False 

    def decideCreekLowLog(self):
        if isCreekLow() and not self.wasCreekLow:
            self.wasCreekLow = True
            return True
        elif not isCreekLow():
            wasCreekLow = False
            return False
        return False

def isCreekLow():
    isCreekLow = False 
    return isCreekLow 

   
