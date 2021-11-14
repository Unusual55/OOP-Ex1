

class Call:
    def __init__(self, time, src, dst):
        self.time = time
        self.src = src
        self.dst = dst
        self.allocated_elevator = None
        self.direction = dst - src
        pass
