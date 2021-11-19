import pandas as pd
from Building import Building
from Call import Call
from Elevator import Elevator
from Route import Route
import math
import threading
from numba import jit, prange
import functools
import re
import cProfile
class Controller:
    #Dictionary that contain the names of the fields that we will read from the .csv file
    #This function set the id of every selected call to -1- the default id before the allocation
    __columns_headers = ['elevator-call', 'time', 'source',
                         'destination', 'status', 'allocated-elevator']
    #This function initialize the Controller object
    def __init__(self, calls_log: pd.DataFrame):
        self.calls_log = calls_log
        self.calls_data = self.calls_log[[
            'time', 'source', 'destination', 'allocated-elevator']]

        self.calls = [Call(row["time"], row["source"], row["destination"], i)
                      for i, row in self.calls_data.iterrows()]
        
        self.allocated_elevators = [-1]*len(self.calls)

    #This function get the id of a call and the id of an elevator, and set the value at
    #allocated_elevators at index call_id to elevator_id, so we can later export it to .csv
    #file that contains the allocated elevator's id    
    def allocate_elevator(self, call_id: int, elevator_id: int):
        self.allocated_elevators[call_id] = elevator_id

    #This function run the allocation simulator, for each call it select the optimal elevator to
    #handle this call and allocate it to this call
    @functools.lru_cache(maxsize=128)
    def allocate(self, building: Building):
        elevs = building.elevators
        sp_avg = (sum([e.speed for e in elevs])/len(elevs))*(building.number_of_floors*0.14)
        for call in reversed(self.calls):
            m = math.inf
            id = -1
            for i in range(building.number_of_elevators):
                t = elevs[i].route.check_insertion_delay_factor(call)
                if t < m:
                    m = t
                    id = elevs[i].elevator_id
            building.elevators[id].route.create_dummy_course(call)
            self.allocate_elevator(call.id, id)

    #This function get a path to .csv file that contains the list of calls data, and parse it to
    #list of Call objects
    @classmethod
    def from_csv(cls, file_name: str):
        return cls(pd.read_csv(file_name, names=cls.__columns_headers))
    
    #This function gets a name of the outpus .csv file, it write the data of the calls and
    #allocated elevator in the correct format so the simulator will be able to accept the .csv file
    def to_csv(self, file_name: str):
        self.calls_log["allocated-elevator"] = self.allocated_elevators
        self.calls_log.to_csv(file_name, index=False, header=False)