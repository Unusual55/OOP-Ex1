class OBuilding:
    def __init__(self, min, max, elevatornumber, elevators, name):
        self.minFloor = min
        self.maxFloor = max
        self.elevatornumber = elevatornumber
        self.elevatorlist = []
        self.buildingname = name
        for x in elevators:
            self.__addElevator(self, x)


    def __addElevator(self,elev):
        self.elevatorlist.append(self, elev)

    def getElevator(self,i):
        return self.elevatorlist.__getitem__(self, i)

    def getMinFloor(self):
        return self.minFloor

    def getMaxFloor(self):
        return self.maxFloor

    def getNumberOfElevators(self):
        return self.elevatornumber

    def getBuildingName(self):
        return self.buildingname

    def getFloorNumber(self):
        return abs(self.maxFloor-self.minFloor)



