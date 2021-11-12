class OBuilding:
    def __init__(self, min_floor, max_floor, elevators_amount):
        self.min_floor = min_floor if min_floor < max_floor else max_floor
        self.max_floor = max_floor if max_floor > min_floor else min_floor

        self.elevators_amount = elevators_amount
        self.elevatorslist = []
        self.buildingname = None
        self.calls = []

        self.number_of_floors = abs(self.max_floor - self.min_floor)

    def add_elevator(self, elev):
        self.elevatorslist.append(elev)
        return self

    def get_elevator(self, i):
        return self.elevatorslist[i]

    def add_calls(self, calls):
        for x in calls:
            self.calls.append(x)
