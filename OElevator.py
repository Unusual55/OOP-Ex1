class OElevator:
    def __init__(self, elevatorID, speed, minFloor, maxFloor, closeTime, openTime, startTime, stopTime):
        self.id = elevatorID
        self.minFloor = minFloor
        self.maxFloor = maxFloor
        self.openTime = openTime
        self.closeTime = closeTime
        self.startTime = startTime
        self.stopTime = stopTime
        self.speed = speed
        self.TPF = (1/self.speed)
        self.state = None
        self.pos = None
        self.nextstop = None

    def GetTimeForOpen(self):
        return self.openTime

    def GetTimeForClose(self):
        return self.closeTime

    def GetTimeForStart(self):
        return self.startTime

    def GetTimeForStop(self):
        return self.stopTime

    def GetSpeed(self):
        return self.speed

    def GetTimePerFloor(self):
        return self.TPF

    def GetMinFloor(self):
        return self.minFloor

    def GetMaxFloor(self):
        return self.maxFloor

    def GetID(self):
        return self.id

    def GetState(self):
        return self.state

    def GetPos(self):
        return self.pos

    def goto(self, floor):
        # nextState = 0
        # if(floor > self.pos):
        #     nextState = 1
        # elif(floor < self.pos):
        #     nextState = -1
        # self.state = nextState
        self.state = 1 if floor > self.pos else (-1 if floor < self.pos else 0)
        self.nextstop = floor

    def stop(self, floor):
        if (self.state == 1):
            if(self.pos < floor and floor < self.nextstop):
                self.nextstop = floor
            else:
                print(
                    "Invalid stop action, the floor is not between position and destenation")
        elif(self.state == -1):
            if(self.pos > floor and floor > self.nextstop):
                self.nextstop = floor
            else:
                print(
                    "Invalid stop action, the floor is not between position and destenation")
        else:
            print(
                "Invalid stop action, stop is not available when the elevator is not moving")
