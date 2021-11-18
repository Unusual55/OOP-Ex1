from Call import Call
from Node import Node, Type
from Elevator import Elevator, Direction
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
    def case_check(self, vec: Vector, course: list):
        elev_dir = self.get_state(vec.incoming, course)
        call_dir = math.copysign(1.0, vec.src.floor - vec.dst.floor)
        elev_pos = self.future_position(vec.incoming, course)
        
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
    def calc_route_time(vect: list):
        return sum([v.dst.time - v.incoming.time for v in vect])
    
    def create_dummy_vectors(self):
        return [copy(v) for v in self.call_pointers]
        # return copy(self.call_pointers)

    def create_basic_course(self, vec:Vector):
        course = []
        course.insert(0,vec.incoming)
        if len(self.call_pointers)>=1:   
            for i in range(len(self.call_pointers)):
                course.append(self.call_pointers[i].incoming)
        return course

    def add_vector_to_route(self, vec: Vector, course: list):
        info = self.get_insertion_index(vec, course)
        for i in range(info[0],info[1]):
            course[i].increase_by_split_cases(self.stop_const.get('full_break'))
        for i in range(info[1]):
            course[i].increase_by_split_cases(self.stop_const.get('full_break'))
        vec.src.time += info[2]
        vec.dst.time += info[3]
        course.insert(info[0], vec.src)
        course.insert(info[1], vec.dst)
    
    def create_dummy_course(self, c: Call):
        course = self.create_basic_course(Vector(c))
        vectors = self.create_dummy_vectors()
        vec = Vector(c)
        vectors.insert(0, vec)
        for vector in vectors:
            self.add_vector_to_route(vector, course)
        return (course, vectors, Route.calc_route_time(vectors))

    def get_offer(self, c: Call):
        return self.create_dummy_course(c)[2]

    def set_new_route(self, c: Call):
        tup = self.create_dummy_course(c)
        self.timed_course = tup[0]
        self.call_pointers = tup[1]


    def future_position(self, incoming_node: Node, course: list):
        state = self.get_state(incoming_node, course)
        inc_index = course.index(incoming_node)
        i = inc_index
        while i-1>0 and course[i-1].type == Type.incoming:
            i -= 1
        last_floor = course[i].floor
        if state == 0:
            return last_floor
        next_time = incoming_node.time
        curr_time = course[i].time
        dt = abs(next_time - curr_time)
        dt -= self.stop_const.get("start_course") # Add the time it takes to close the doors and start the elevator
        return last_floor + state * (dt * self.speed_const.get("speed"))

    #This function calculates the time which take to this call to complete as well as how much delay factor will be caused if we add this call to the list
    def easy_case_same_diretion(self, vec: Vector, course: list):
        pos = self.future_position(vec.incoming, course)
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
        while i<len(course) and inc_node.time>course[i].time:
            i+=1
        inc_index = i    
        while i < len(course) and ((dir and course[i].floor >= src_node.floor) or ((not dir) and course[i].floor <= src_node.floor)):
            src_delay += 1
            i += 1
        src_index = i
        src_time = src_delay*self.stop_const.get('full_break')+abs(src-pos)*self.speed_const.get('tpf') + self.stop_const.get('end_course')
        while i < len(course) and ((dir and course[i].floor >= dst_node.floor) or ((not dir) and course[i].floor <= dst_node.floor)):
            dst_delay += 1
            i += 1
        dst_index = i
        delay_factor = (2*src_delay +dst_delay)*self.stop_const.get('full_break')
        return (src_index, dst_index, src_time , delay_factor + dist)

    def easy_case_inverse_direction(self, vec: Vector, course: list):
        pos = self.future_position(vec.incoming, course)
        inc_node = vec.incoming
        src_node = vec.src
        dst_node = vec.dst
        src = src_node.floor
        dst = dst_node.floor
        inc_index = course.index(inc_node)
        dir = src-pos > 0
        i = inc_index
        src_delay = 0
        while i < len(course) and ((dir and course[i].floor >= src_node.floor) or ((not dir) and course[i].floor <= src_node.floor)):
            src_delay += 1
            i += 1
        src_index = i
        src_time = src_delay*self.stop_const.get('full_break')+abs(src-pos)*self.speed_const.get('tpf') + self.stop_const.get('end_course')
        dst_delay = 0
        turn = self.find_turning_point(i, course)
        while i < turn:
            i += 1
            dst_delay += 1
        dir = not dir
        while i < len(course) and ((dir and course[i].floor >= dst_node.floor) or ((not dir) and course[i].floor <= dst_node.floor)):
            dst_delay += 1
            i += 1
        dst_index = i
        dist = (abs(src-pos)+abs(turn-src)+abs(turn-dst))*self.speed_const.get('tpf')
        dist += (2*src + dst_delay + 1) * self.stop_const.get('full_break')
        return(src_index, dst_index, src_time , dist)
        
    def hard_case_missed_floor(self, vec: Vector, course: list):
        pos = self.future_position(vec.incoming, course)
        inc_node = vec.incoming
        src_node = vec.src
        dst_node = vec.dst
        src = src_node.floor
        dst = dst_node.floor
        inc_index = course.index(inc_node)
        dir = src-pos > 0
        i = inc_index
        src_delay = 0
        dst_delay = 0
        turn1 = self.find_turning_point(i, course)
        while i < turn1:
            i += 1
            src_delay += 1
        dir = src - pos > 0
        while i < len(course) and ((dir and course[i].floor >= src_node.floor) or ((not dir) and course[i].floor <= src_node.floor)):
            src_delay += 1
            i += 1
        src_index = i
        turn2 = self.find_turning_point(i, course)
        while i < turn2:
            i += 1
            dst_delay += 1
        while i < len(course) and ((dir and course[i].floor >= dst_node.floor) or ((not dir) and course[i].floor <= dst_node.floor)):
            dst_delay += 1
            i += 1
        dst_index = i
        turn_floor1 = course[turn1].floor
        turn_floor2 = course[turn2].floor
        src_time =(src_delay*self.stop_const.get('full_break')+(abs(turn1-pos)+abs(turn1-src))*self.speed_const.get('tpf')+self.stop_const.get('end_course'))
        dist = (abs(turn_floor1-pos)+abs(turn_floor1-src)+abs(src-turn_floor2)+abs(dst-turn_floor2))*self.speed_const.get('tpf')
        delay_factor = (2*src_delay + dst_delay)*self.stop_const.get('full_break')
        return (src_index, dst_index, src_time , dist + delay_factor)

    def get_sorted_nodelist(self):
        li = [] 
        for i in self.call_pointers:
            li.append(i[0])
            li.append(i[1])
        return sorted(li, key=lambda x: x.time, reverse=True)

    def find_turning_point(self, i: int, course: list):
        calls = course[i:]
        if len(calls) < 2:
            return -1
        sign = math.copysign(1.0, calls[0].floor - calls[1].floor)
        for j in range(1, len(calls)-1):
            s = math.copysign(1.0, calls[j].floor - calls[j+1].floor)
            if s * sign < 0:
                return i + j + 1
            sign = s
        return -1

    def get_state(self, incoming: Node, course: list):
        inc_index = course.index(incoming)
        if inc_index == len(course)-1:
            return Direction.IDLE
        i = inc_index
        while i-1>0 and course[i].type == Type.incoming:
            i -=1
        last_Stop_floor = course[i].floor
        j = inc_index
        while j+1< len(course) and course[j].type == Type.incoming:
            j += 1
        next_stop_floor = course[j].floor
        if next_stop_floor > last_Stop_floor:
            return Direction.UP
        return Direction.DOWN

    def get_insertion_index(self, vec: Vector, course: list):
        case = self.case_check(vec, course)
        if case == 1:
            tup = self.easy_case_same_diretion(vec, course)
        elif case == 2:
            tup = self.easy_case_inverse_direction(vec, course)
        else:
            tup = self.hard_case_missed_floor(vec, course)
        return tup
        

    
    