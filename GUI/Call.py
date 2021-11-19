import math

class Call:
    def __init__(self, time, src, dst, id):
        self.time = time
        self.src = src
        self.dst = dst
        self.allocated_elevator = None
        self.direction = math.copysign(1, dst - src)
        self.id = id

    #TODO: add id property in the csv parser
