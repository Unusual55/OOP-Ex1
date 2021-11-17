from Call import Call
from Node import Node, Type
from Elevator import Direction, Elevator
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
    
    # TODO: add case if elev_pos == src.floor
    def case_check(self, vec: Vector):
        elev_dir = self.get_state(vec.incoming)
        call_dir = math.copysign(1.0, vec.src.floor - vec.dst.floor)
        elev_pos = self.future_position(vec.incoming)
        
        # Can we pickup the call?
        if elev_dir > 0:
            if elev_pos < vec.src.floor:
                if vec.src.floor < vec.dst.floor:
                    return 1
                else:
                    return 2
            else:
                return 3
        elif elev_dir < 0:
            if elev_pos > vec.src.floor:
                if vec.src.floor > vec.dst.floor:
                    return 1
                else:
                    return 2
            else:
                return 3
        else:
            if call_dir > 0:
                if elev_pos < vec.src.floor:
                    if vec.src.floor < vec.dst.floor:
                        return 1
                    else:
                        return 2
            else:
                if elev_pos > vec.src.floor:
                    if vec.src.floor>vec.dst.floor:
                        return 1
                    else: 
                        return 2
    @staticmethod        
    def calc_route_time(self, vect: list):
        return sum([v.dst.time - v.incoming.time for v in vect])
    
    def create_dummy_vectors(self):
        return copy(self.call_pointers)

    def create_basic_course(self, vec:Vector):
        for vec in self.call_pointers:
            vec.reset()
        course = []
        course.append(vec.incoming)
        for vec in self.call_pointers:
            course.append(vec.incoming)
        return course

    def add_vector_to_route(self, vec: Vector, course: list):
        info = self.get_insertion_index(vec)
        for i in range(info[1],info[2]):
            course[i].increase_by(self.speed_const)
        for i in range(info[2]):
            course[i].increase_by(self.speed_const)
        course.insert(info[0], info[2])
        course.inser(info[1], info[3])
    
    def create_dummy_course(self, c: Call):
        course = self.create_basic_course(c)
        vectors = self.create_dummy_vectors()
        vec = Vector(c)
        vectors.insert(0, vec)
        for vector in vectors:
            self.add_vector_to_route(vector, course)
        return (course, vectors, Route.calc_route_time(self, vectors))

    def get_offer(self, c: Call):
        return self.create_dummy_course(c)[2]

    def set_new_route(self, c: Call):
        tup = self.create_dummy_course(c)
        self.timed_course = tup[0]
        self.call_pointers = tup[1]


    def future_position(self, incoming_node: Node):
        state = self.get_state(incoming_node)
        inc_index = self.timed_course.index(incoming_node)
        i = inc_index
        while i-1>0 and self.timed_course[i-1].type == Type.incoming:
            i -= 1
        last_floor = self.timed_course[i].floor
        if state == 0:
            return last_floor
        next_time = incoming_node.time
        curr_time = self.timed_course[i].time
        dt = abs(next_time - curr_time)
        dt -= self.stop_const["start_course"] # Add the time it takes to close the doors and start the elevator
        return self.last_stop_node.floor + state * (dt * self.speed_const["speed"])

    # def reroute(self, c: Call):
    #     dummy_vectors = self.create_dummy_vectors()
    #     v = Vector(c)
    #     dummy_vectors.insert(0,v)
    #     for v in dummy_vectors:
    #         v.


    #This function calculates the time which take to this call to complete as well as how much delay factor will be caused if we add this call to the list
    def easy_case_same_diretion(self, vec: Vector):
        pos = self.future_position(vec.incoming)
        inc_node = vec.incoming
        src_node = vec.src
        dst_node = vec.dst
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
        while (dir and self.timed_course[i].floor >= src_node.floor) or ((not dir) and self.timed_course[i].floor <= src_node.floor):
            src_delay += 1
            i += 1
        src_index = i
        src_time = src_delay*self.speed_const.get('full_break')+abs(src-pos)*self.speed_const.get('tpf') + self.stop_const.get('end_course')
        while (dir and self.timed_course[i].floor >= dst_node.floor) or ((not dir) and self.timed_course[i].floor <= dst_node.floor):
            dst_delay += 1
            i += 1
        dst_index = i
        delay_factor = (2*src_delay +dst_delay)*self.stop_const.get('full_break')
        return (src_index, dst_index, src_time , delay_factor + dist)

    def easy_case_inverse_direction(self, vec: Vector):
        pos = self.future_position(vec.incoming)
        inc_node = vec.incoming
        src_node = vec.src
        dst_node = vec.dst
        src = src_node.floor
        dst = dst_node.floor
        inc_index = self.timed_course.index(inc_node)
        dir = src-pos > 0
        i = inc_index
        src_delay = 0
        while (dir and self.timed_course[i].floor >= src_node.floor) or ((not dir) and self.timed_course[i].floor <= src_node.floor):
            src_delay += 1
            i += 1
        src_index = i
        src_time = src_delay*self.speed_const.get('full_break')+abs(src-pos)*self.speed_const.get('tpf') + self.stop_const.get('end_course')
        dst_delay = 0
        turn = self.find_turning_point(i)
        while i < turn:
            i += 1
            dst_delay += 1
        dir = not dir
        while (dir and self.timed_course[i].floor >= dst_node.floor) or ((not dir) and self.timed_course[i].floor <= dst_node.floor):
            dst_delay += 1
            i += 1
        dst_index = i
        dist = (abs(src-pos)+abs(turn-src)+abs(turn-dst))*self.speed_const.get('tpf')
        dist += (2*src + dst_delay + 1) * self.stop_const.get('full_break')
        return(src_index, dst_index, src_time , dist)
        
    def hard_case_missed_floor(self, vec: Vector, pos):
        pos = self.future_position(vec.incoming)
        inc_node = vec.incoming
        src_node = vec.src
        dst_node = vec.dst
        src = src_node.floor
        dst = dst_node.floor
        inc_index = self.timed_course.index(inc_node)
        dir = src-pos > 0
        i = inc_index
        src_delay = 0
        dst_delay = 0
        turn1 = self.find_turning_point(i)
        while i < turn1:
            i += 1
            src_delay += 1
        dir = src - pos > 0
        while (dir and self.timed_course[i].floor >= src_node.floor) or ((not dir) and self.timed_course[i].floor <= src_node.floor):
            src_delay += 1
            i += 1
        src_index = i
        turn2 = self.find_turning_point(i)
        while i < turn2:
            i += 1
            dst_delay += 1
        while (dir and self.timed_course[i].floor >= dst_node.floor) or ((not dir) and self.timed_course[i].floor <= dst_node.floor):
            dst_delay += 1
            i += 1
        dst_index = i
        turn_floor1 = self.timed_course[turn1].floor
        turn_floor2 = self.timed_course[turn2].floor
        src_time =(src_delay*self.stop_const.get('full_break')+(abs(turn1-pos)+abs(turn1-src))*self.speed_const.get('tpf')+self.stop_const.get('end_course'))
        dist = (abs(turn_floor1-pos)+abs(turn_floor1-src)+abs(src-turn_floor2)+abs()+abs(dst-turn_floor2))*self.speed_const.get('tpf')
        delay_factor = (2*src_delay + dst_delay)*self.stop_const.get('full_break')
        return (src_index, dst_index, src_time , dist + delay_factor)

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

    def get_state(self, incoming: Node):
        inc_index = self.timed_course.index(incoming)
        if inc_index == len(self.timed_course)-1:
            return Direction.IDLE
        i = inc_index
        while i-1>0 and self.timed_course[i].type == Type.incoming:
            i -=1
        last_Stop_floor = self.timed_course[i].floor
        j = inc_index
        while j+1< len(self.timed_course) and self.timed_course[j].type == Type.incoming:
            j += 1
        next_stop_floor = self.timed_course[j].floor
        if next_stop_floor > last_Stop_floor:
            return Direction.UP
        return Direction.DOWN

    def get_insertion_index(self, vec: Vector):
        case = self.case_check(vec)
        if case == 1:
            tup = self.easy_case_same_diretion(vec)
        elif case == 2:
            tup = self.easy_case_inverse_direction(vec)
        else:
            tup = self.hard_case_missed_floor(vec)
        return tup
        
    # # TODO: We don't consider if the stop already exists in the stops list, this could cause problems since the elevator would have the floor multiple times
    # def minimal_distance_index(self, stop):
    #     if len(self) == 0:
    #         return 0
    #     stops = self.stops.copy()
    #     dists = [sum(Route.calc_distances(stops[:i] + [stop] + stops[i:])) for i in range(len(stops)+1)]
    #     return dists.index(min(dists))


    
    