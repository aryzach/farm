import toolz
import time
from pythonping import ping
import re
import json
from pathlib import Path
import os
import netifaces as ni
from pyunifi.controller import Controller
import config 

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

wan = {'WAN coastside':'8.8.8.8'}
wan2 = {'WAN satellite': '8.8.8.8'}
        

cameras = toolz.keymap(lambda x : 'cam ' + x, (toolz.valmap(lambda x : IPprefix + x, {
        'acorn':'237',
        'CSA':'235',
        'Farm Store':'229',
        'front gate':'234',
        'goat outdoor':'236',
        'coop indoor':'40',
        'coop outdoor':'42',
        'office':'48',
        'property':'126',
        'Chick Big Hutch':'137',
        'Creek':'130'
        })))

'''
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
        'water tank':'18'
        })
'''

nb = toolz.keymap(lambda x : 'NB ' + x, (toolz.valmap(lambda x : IPprefix + x, {
        'farmhouse':'21',
        'top of hill':'22',
        'reciever in barn':'23',
        'front gate':'24',
        'csa gate':'25',
        'hill to water tank':'26',
        'barn to office':'27',
        'office':'28',
        'coops':'29',
        'barn to creek':'30',
        'creek':'31',
        'coastside':'32',
        'water tank':'33',
        'water tank to coastside':'34'
        })))


def getLAN():
    c = Controller('192.168.1.44', 'twistedfields', config.PASSWORD,ssl_verify=False)
    lan = {}
    aps = c.get_aps()
    for ap in aps:
        try:
            name = ap.get('name')
        except:
            name = 'no name'
        ip = ap['ip']
        lan['AP ' + name] = ip
    return lan

lan = getLAN()


destinations = {**wan,**wan2,**lan,**cameras,**nb}


while True:
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
    entry = {time.time() : results}
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


