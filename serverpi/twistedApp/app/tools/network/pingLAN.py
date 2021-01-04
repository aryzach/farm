import toolz
import time
from pythonping import ping
from time import gmtime, strftime, localtime
import re
import json
from pathlib import Path
import os
import netifaces as ni

# frequency of pings in seconds
FREQUENCY = 60*10 

PINGFILE = os.path.join(os.path.dirname(__file__), 'ping.json')

def getWLAN1_IP():
    try:
        WLAN1_IP = ni.ifaddresses('wlan1')[ni.AF_INET][0]['addr']
        return WLAN1_IP
    except:
        print('not getting wlan1 IP address')
        return None

IPprefix = '192.168.1.'

wan = {'coastsideWAN':'8.8.8.8'}
wan2 = {'satelliteWAN': '8.8.8.8'}
        

cameras = toolz.valmap(lambda x : IPprefix + x, {
        'acorn cam':'237',
        'CSA cam':'235',
        'Farm Store cam':'229',
        'front gate cam':'234',
        'goat outdoor cam':'236',
        'coop indoor cam':'40',
        'coop outdoor cam':'42',
        'office cam':'48',
        'property cam':'218'
        })

lan = toolz.valmap(lambda x : IPprefix + x, {
        'security gateway':'1',
        'barn switch':'177',
        'coastside switch':'228',
        'farmhouse switch':'155',
        'office switch':'176',
        'back of farmhouse':'153',
        'barn interior':'14',
        'barn media hp':'88',
        'big field hp':'10',
        'creek':'109',
        'csa gate hp':'238',
        'farm store':'254',
        'farmhouse dining':'11',
        'farmhouse exterior hp':'7',
        'front gate hp':'233',
        'goatbarn interior':'222',
        'guest house':'19',
        'office':'158',
        'top of hill':'16',
        'water tank':'18',
        'farmhouse NB':'21',
        'top of hill NB':'22',
        'reciever in barn NB':'23',
        'front gate NB':'24',
        'csa gate NB':'25',
        'hill to water tank NB':'26',
        'water tanks NB':'27',
        'coops NB':'29',
        'barn to creek NB':'30',
        'creek NB':'31',
        'water tank to coastside NB':'33',
        'coastside NB':'34'
        })

destinations = {**lan,**wan,**wan2,**cameras}
print(destinations)



while True:
    currentTime = strftime("%Y-%m-%d %H:%M:%S", localtime())
    results = {}
    for destination in destinations:
        try:
            if destination == 'satelliteWAN':
                WLAN1_IP = getWLAN1_IP()
                result = ping(destinations[destination],source=WLAN1_IP)
            else:
                result = ping(destinations[destination])
        except:
            result = 2000
        if result != 2000:
            result = result.rtt_avg_ms
        results[destination] = result 
        entry = {currentTime : results}
    if Path(PINGFILE).exists():
        with open(PINGFILE) as f:
            allData = json.load(f)
    else:
        allData = {}
    allData.update(entry)
    with open(PINGFILE,"w") as f:
        f.seek(0)
        json.dump(allData, f)
    time.sleep(FREQUENCY)


