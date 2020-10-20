from time import time, mktime

RECENT_CUTOFF = 20 

def isRecent(saved):
    dif = time() - saved 
    return dif < RECENT_CUTOFF 


