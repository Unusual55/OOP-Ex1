import time


class OCallForElevator:
    enum
    def __init__(self, time, src, dest):
        self.__state = 0
        self.__src = src
        self.__dest = dest
        self.__statechanges = [time, -1, -1, -1]
        self.__type = 0
        if (src < dest):
            __type = 1
        else:
            __type = -1
        self.__elevator = -1

    def getstate(self):
        return self.__state

    def gettime(self, state):
        return self.__statechanges[state]

    def getsrc(self):
        return self.__src

    def getdest(self):
        return self.__dest

    def gettype(self):
        return self.__type

    def allocatedto(self):
        return self.__elevator

    def allocateto(self, elev):
        self.__elevator = elev
        self.__state = 1
        self.__statechanges[1] = time.clock()

    def reachedsrc(self):
        self.__statechanges[2] = time.clock()
        self.__state = 2

    def reacheddest(self):
        self.__statechanges[3] = time.clock()
