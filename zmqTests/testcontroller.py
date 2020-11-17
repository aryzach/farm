import time
from datetime import datetime


# init list with pin numbers

outpins = [14,15]
inpins = [2] 

lowAgPin = 14
medAgPin = 15


# global vars!
wasCreekLow = False

# loop through pins and set mode and state to 'low'


def isCreekLow():
    isCreekLow = True 
    shouldLog = decideCreekLowLog(isCreekLow)
    return isCreekLow 

def decideCreekLowLog(isCreekLow):
    if isCreekLow and not wasCreekLow:
        wasCreekLow = True
        return True
    elif not isCreekLow:
        wasCreekLow = False
        return False

    
