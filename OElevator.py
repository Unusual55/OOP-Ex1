class OElevator:
    def __init__(self, id, min, max, open, close, start, stop, speed, state, pos, nextstop):
        self.id = id
        self.minFloor = min
        self.maxFloor = max
        self.openTime = open
        self.closeTime = close
        self.startTime = start
        self.stopTime = stop
        self.speed = speed
        self.tpf = (1/self.speed)
        self.state = state
        self.pos = pos
        self.nextstop = nextstop

    def gettimeforopen(self):
        return self.openTime

    def gettimeforclose(self):
        return self.closeTime

    def gettimeforstart(self):
        return self.startTime

    def gettimeforstop(self):
        return self.stopTime

    def getspeed(self):
        return self.speed

    def gettimeperfloor(self):
        return self.tpf

    def getminfloor(self):
        return self.minFloor

    def getmaxfloor(self):
        return self.maxFloor

    def getid(self):
        return self.id
