class OBuilding:
    def __init__(self, minFloor, maxFloor, elevatorsamount):
        self.minFloor = minFloor
        self.maxFloor = maxFloor
        self.elevatorsamount = elevatorsamount
        self.elevatorslist = []
        self.buildingname = None
        self.calls = []

    def AddElevator(self, elev):
        self.elevatorslist.append(elev)

    def GetElevator(self, i):
        return self.elevatorslist[i]

    def GetMinFloor(self):
        return self.minFloor

    def GetMaxFloor(self):
        return self.maxFloor

    def GetNumberOfElevators(self):
        return self.elevatorsamount

    def GetFloorNumber(self):
        return abs(self.maxFloor - self.minFloor)

    def AddCalls(self, calls):
        for x in calls:
            self.calls.append(x)
