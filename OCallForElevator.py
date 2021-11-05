import time


class OCallForElevator:
    def __init__(self, time, src, dest):
        self.__state = 0
        self.__src = src
        self.__dest = dest
        self.__statechanges = [time, -1, -1, -1]
        self.__type = 1 if src < dest else -1
        self.__elevator = -1

    def GetState(self):
        return self.__state

    def GetTime(self, state):
        return self.__statechanges[state]

    def GetSrc(self):
        return self.__src

    def GetDest(self):
        return self.__dest

    def GetType(self):
        return self.__type

    def AllocatedTo(self):
        return self.__elevator

    def AllocateTo(self, elev):
        self.__elevator = elev
        self.__state = 1
        self.__statechanges[1] = time.time()

    def ReachedSrc(self):
        self.__statechanges[2] = time.time()
        self.__state = 2

    def ReachedDest(self):
        self.__statechanges[3] = time.time()
