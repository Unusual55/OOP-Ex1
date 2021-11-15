

class Call:
    def init__(self, time, src, dst):
        self.time = time
        self.src = src
        self.dst = dst
        self.allocated_elevator = None
        self.direction = dst - src
        self.id = 0
        pass

    #TODO: add id property in the csv parser
