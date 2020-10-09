from pythonping import ping
import time
from time import gmtime, strftime, localtime



while True:
    print("At time: ", strftime("%Y-%m-%d %H:%M:%S", localtime()))
    ping('192.168.1.121', verbose=True)
    time.sleep(60*60)


