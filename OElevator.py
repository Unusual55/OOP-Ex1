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

    def getstate(self):
        return self.state

    def getdest(self):
        return self.state

    def getpos(self):
        return self.pos

    def goto(self, floor):
        nextstate = 0
        if(floor>self.pos):
            nextstate = 1
        elif(floor<self.pos):
            nextstate = -1
        self.state = nextstate
        self.nextstop = floor

    def stop(self, floor):
        if (self.state==1):
            if(self.pos<floor and floor<self.nextstop):
                self.nextstop = floor
            else:
                print("Invalid stop action, the floor is not between position and destenation")
        elif(self.state==-1):
            if(self.pos>floor and floor>self.nextstop):
                self.nextstop = floor
            else:
                print("Invalid stop action, the floor is not between position and destenation")
        else:
            print("Invalid stop action, stop is not available when the elevator is not moving")

