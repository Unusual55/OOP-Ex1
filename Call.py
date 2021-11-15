import math

class Call:
    def __init__(self, time, src, dst):
        self.time = time
        self.src = src
        self.dst = dst
        self.allocated_elevator = None
        self.direction = math.copysign(1, dst - src)
        self.state_change = [self.time, math.ceil(self.time), None, None, None, None, None, None] 
        pass
