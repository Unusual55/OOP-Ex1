class OElevator:
    def __init__(self, elevator_id, speed, min_floor, max_floor, close_time, open_time, start_time, stop_time):
        self.elevator_id = elevator_id
        self.speed = speed
        self.min_floor = min_floor
        self.max_floor = max_floor
        self.close_time = close_time
        self.open_time = open_time
        self.start_time = start_time
        self.stop_time = stop_time
        self.TPF = (1/self.speed)
        self.state = None
        self.pos = None
        self.next_stop = None

    def goto(self, floor):
        # nextState = 0
        # if(floor > self.pos):
        #     nextState = 1
        # elif(floor < self.pos):
        #     nextState = -1
        # self.state = nextState
        self.state = 1 if floor > self.pos else (-1 if floor < self.pos else 0)
        self.next_stop = floor

    def stop(self, floor):
        if (self.state == 1):
            if(self.pos < floor and floor < self.next_stop):
                self.next_stop = floor
            else:
                print(
                    "Invalid stop action, the floor is not between position and destenation")
        elif(self.state == -1):
            if(self.pos > floor and floor > self.next_stop):
                self.next_stop = floor
            else:
                print(
                    "Invalid stop action, the floor is not between position and destenation")
        else:
            print(
                "Invalid stop action, stop is not available when the elevator is not moving")
