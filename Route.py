from typing import Tuple
from Call import Call
from Node import Node, Type
from Elevator import Elevator
from copy import copy
from Vector import Vector
import math
class Route:
    def __init__(self, e: Elevator) -> None:
        self.call_pointers = []
        self.timed_course = [] # we might need to create linkedlist of nodes so we can seperate the route data structure from the course
        self.stop_const = {'start_course': e.close_time + e.start_time, 'end_course': e.stop_time + e.open_time, 'full_break': e.open_time + e.close_time + e.start_time + e.stop_time}
        self.speed_const = {'speed': e.speed, 'tpf': 1/e.speed}
        self.count = 0
        
    def create_dummy_vectors(self):
        return copy(self.call_pointers)

    def add_vector_to_route(self, c: Call):
        pass

    # def Route_Offer(self, c: Call):
    #     pass

    # def route_optimal_now(self):
    #     pass

    # def reroute(self, c: Call):
    #     dummy_vectors = self.create_dummy_vectors()
    #     v = Vector(c)
    #     dummy_vectors.insert(0,v)
    #     for v in dummy_vectors:
    #         v.


    #This function calculates the time which take to this call to complete as well as how much delay factor will be caused if we add this call to the list
    def easy_case_same_diretion_up(self, pos: int, vec: Vector):
        inc_node = vec[0]
        src_node = vec[1]
        dst_node = vec[2]
        src = src_node.floor
        dst = dst_node.floor
        dist = (abs(src-pos)+abs(dst-src))*self.speed_const.get('tpf') + self.stop_const.get('full_break')
        src_delay = 0
        dst_delay = 0
        i = 0
        dir = src-pos>0
        dire = math.copysign(1, src - pos)
        while i<len(self.timed_course) and inc_node.time>self.timed_course[i].time:
            i+=1
        inc_index = i
        
        # while self.timed_course[i].floor >= dire*src_node.floor:
        #     src_delay += 1
        #     i += 1
        # while self.timed_course[i].floor >= dire*dst_node.floor:
        #     dst_delay += 1
        #     i += 1
        
        while (dir and self.timed_course[i].floor >= src_node.floor) or ((not dir) and self.timed_course[i].floor <= src_node.floor):
            src_delay += 1
            i += 1
        while (dir and self.timed_course[i].floor >= dst_node.floor) or ((not dir) and self.timed_course[i].floor <= dst_node.floor):
            dst_delay += 1
            i += 1

        #region
        # if dir:
        #     while self.timed_course[i].floor >= src_node.floor:
        #         src_delay += 1
        #         i += 1
        #     while self.timed_course[i].floor >= dst_node.floor:
        #         dst_delay += 1
        #         i += 1
        # else:
        #      while self.timed_course[i].floor <= src_node.floor:
        #         src_delay += 1
        #         i += 1
        #      while self.timed_course[i].floor <= dst_node.floor:
        #         dst_delay += 1
        #         i += 1
        #endregion

        delay_factor = (2*src_delay +dst_delay)*self.stop_const.get('full_break')
        return delay_factor + dist

    def easy_case_same_inverse_direction_pickup_time_calc(self, vec: Vector):
        pass

    def hard_case_missed_floor_time_calc(self, vec: Vector):
        pass

    def get_sorted_nodelist(self):
        li = [] 
        for i in self.call_pointers:
            li.append(i[0])
            li.append(i[1])
        return sorted(li, key=lambda x: x.time, reverse=True)

    def find_turning_point(self, i: int):
        if len(self.timed_course) < 2:
            return -1
        calls = self.timed_course[i:]
        sign = math.copysign(1.0, calls[0].floor - calls[1].floor)
        for j in range(1, len(calls)-1):
            s = math.copysign(1.0, calls[j].floor - calls[j+1].floor)
            if s * sign < 0:
                return i + j + 1
            sign = s
        return -1

    # def __init__(self, *stops):
    #     self.stops = [c for c in stops]
    #     self.distances = Route.calc_distances(self.stops)
    
    # def add(self, stop):
    #     self.stops.insert(self.minimal_distance_index(stop), stop)
    #     self.distances = Route.calc_distances(self.stops)
        
    # @staticmethod
    # def calc_distances(stops):
    #     return [abs(next - prev) for prev, next in zip(stops, stops[1:])]
    
    # def total_distance(self):
    #     return sum(self.distances)
    
    # # TODO: We don't consider if the stop already exists in the stops list, this could cause problems since the elevator would have the floor multiple times
    # def minimal_distance_index(self, stop):
    #     if len(self) == 0:
    #         return 0
    #     stops = self.stops.copy()
    #     dists = [sum(Route.calc_distances(stops[:i] + [stop] + stops[i:])) for i in range(len(stops)+1)]
    #     return dists.index(min(dists))
    
    
    # def __getitem__(self, index):
    #     return self.stops[index]
    
    # def __len__(self):
    #     return len(self.stops)


    
    