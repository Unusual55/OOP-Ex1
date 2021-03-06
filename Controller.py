import pandas as pd
from Building import Building
from Call import Call
import math
import functools

class Controller:
    __columns_headers = ['elevator-call', 'time', 'source',
                         'destination', 'status', 'allocated-elevator']

    def __init__(self, calls_log: pd.DataFrame):
        self.calls_log = calls_log
        self.calls_data = self.calls_log[[
            'time', 'source', 'destination', 'allocated-elevator']]

        self.calls = [Call(row["time"], row["source"], row["destination"], i)
                      for i, row in self.calls_data.iterrows()]
        
        self.allocated_elevators = [-1]*len(self.calls)

    def allocate_elevator(self, call_id: int, elevator_id: int):
        self.allocated_elevators[call_id] = elevator_id

    @functools.lru_cache(maxsize=128)
    def allocate(self, building: Building):
        elevs = building.elevators
        for call in reversed(self.calls):
            m = math.inf
            elevator_id = -1
            for i in range(building.number_of_elevators):
                t = elevs[i].route.check_insertion_delay_factor(call)
                if t < m:
                    m = t
                    elevator_id = elevs[i].elevator_id
            building.elevators[elevator_id].route.create_dummy_course(call)
            self.allocate_elevator(call.id, elevator_id)

    @classmethod
    def from_csv(cls, file_name: str):
        return cls(pd.read_csv(file_name, names=cls.__columns_headers))
    
    def to_csv(self, file_name: str):
        self.calls_log["allocated-elevator"] = self.allocated_elevators
        self.calls_log.to_csv(file_name, index=False, header=False)