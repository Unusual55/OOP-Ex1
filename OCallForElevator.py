class OCallForElevator:
    def __init__(self, time, src, dest):
        self.state = 0
        self.src = src
        self.dest = dest
        self.statechanges = [time, -1, -1, -1]
        self.type = 0
        if (src < dest):
            type = 1
        else:
            type = -1
        self.elevator = -1

    def allocateto(self, elev):
        self.elevator = elev

    def getstate(self):
        return self.state

    def gettime(self, state):
        return self.statechanges[state]

    def getsrc(self):
        return self.src

    def getdest(self):
        return self.dest

    def gettype(self):
        return self.type

    def allocatedto(self):
        return self.elevator

