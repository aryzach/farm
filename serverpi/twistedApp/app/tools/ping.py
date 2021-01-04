import time
import subprocess
from time import gmtime, strftime, localtime

bigFieldIP = '192.168.1.119'   
waterTankIP = '192.168.1.121'


def getPing(ip):
    try:
        response = subprocess.check_output(
            ['ping', '-c', '3', ip],
            stderr=subprocess.STDOUT,  # get all output
            universal_newlines=True  # return string not bytes
        )
        return True
    except subprocess.CalledProcessError:
        response = None
        return False

getPing("creekpi")




