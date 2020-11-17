import toolz
import time
from pythonping import ping
from time import gmtime, strftime, localtime
import re
import json

# frequency of pings in seconds
FREQUENCY = 60*10 



IPprefix = '192.168.1.'



devices = toolz.valmap(lambda x : IPprefix + x, {
        'security gateway':'1',
        'barn switch':'228',
        'farm store swtich':'230',
        'farmhouse switch':'155',
        'back of farmhouse':'153',
        'barn interior':'14',
        'barn media hp':'88',
        'big field hp':'10',
        'coastside switch':'147',
        'creek':'109',
        'csa gate hp':'238',
        'farm store':'254',
        'farmhouse dining':'11',
        'farmhouse exterior hp':'7',
        'farmhouse upstairs':'17',
        'front gate hp':'233',
        'goatbarn exterior hp':'18',
        'goatbarn interior':'222',
        'guest house':'19',
        'mayas room':'9',
        'mobile coop':'8',
        'office':'158',
        'top of hill':'16',
        'water tank':'146',
        'farmhouse NB':'21',
        'top of hill NB':'22',
        'reciever in barn NB':'23',
        'front gate NB':'24',
        'csa gate NB':'25',
        'hill to water tank NB':'26',
        'water tanks NB':'27',
        'water tank to coastside NB':'28',
        'barn to creek NB':'30',
        'creek NB':'31',
        'coastside NB':'32'
        })





while True:
    currentTime = strftime("%Y-%m-%d %H:%M:%S", localtime())
    results = {}
    for device in devices:
        #print(device)
        result = ping(devices[device]).rtt_avg_ms
        results[device] = result 
        entry = {currentTime : results}
    with open("/home/pi/twistedApp/app/tools/network/ping.json", "w") as f:
        allData = json.load(f)
        allData.update(entry)
        f.seek(0)
        json.dump(allData, f)
    time.sleep(FREQUENCY)


