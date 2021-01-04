import toolz
import time
from pythonping import ping
from time import gmtime, strftime, localtime
import re
import json
from pathlib import Path
import os
import subprocess
import ast

# frequency of pings in seconds
FREQUENCY = 60*60 

TESTSPEEDFILE = os.path.join(os.path.dirname(__file__), 'testspeed.json')


while True:
    currentTime = strftime("%Y-%m-%d %H:%M:%S", localtime())
    result = subprocess.check_output('speedtest --json', shell=True) 
    result = json.loads(result)
    entry = {currentTime : result}
    if Path(TESTSPEEDFILE).exists():
        with open(TESTSPEEDFILE) as f:
            allData = json.loads(f)
    else:
        allData = {}
    allData.update(entry)
    print(allData)
    print(type(allData))
    print(type(result))
    with open(TESTSPEEDFILE,"w") as f:
        f.seek(0)
        json.dump(allData, f)
    time.sleep(FREQUENCY)


