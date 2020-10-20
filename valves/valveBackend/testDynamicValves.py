class Valve:
    def __init__(self, name, time):
        self.name = name
        self.time = time
        self.startTimes = []
        self.stopTimes = []


    def start(self,time):
        self.startTimes.append(time)

    def stop(self,time):
        self.stopTimes.append(time)
        
        
