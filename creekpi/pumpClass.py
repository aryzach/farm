

class Pump(name, pin):
    def __init__(self):
        self.name = name
        self.currentDBState = None
        self.previousDBState = None
        self.pin = pin
    def getDBState(self, pickled):

