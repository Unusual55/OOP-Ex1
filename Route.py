from numpy import extract
from Call import Call
from Node import Node, Type
from Elevator import Direction
from Vector import Vector
import functools
from math import ceil, floor, copysign

class Route:
    def __init__(self, e) -> None:
        import Elevator
        self.call_pointers = []
        self.timed_course = [] # we might need to create linkedlist of nodes so we can seperate the route data structure from the course
        self.stop_const = {'start_course': e.close_time + e.start_time, 'end_course': e.stop_time + e.open_time, 'full_break': e.open_time + e.close_time + e.start_time + e.stop_time}
        self.speed_const = {'speed': e.speed, 'tpf': 1/e.speed}
        self.count = 0
    
    # TODO: add case if elev_pos == src.floor
    def case_check(self, vec: Vector, course: list):
        elev_dir = self.get_state(vec.incoming, course)
        call_dir = copysign(1.0, vec.src.floor - vec.dst.floor)
        elev_pos = self.future_position(vec.incoming, course)
        if len(course) ==1:
            return 0
        # Can we pickup the call?            
        elif elev_dir > 0:
            if elev_pos < vec.src.floor:
                if vec.src.floor < vec.dst.floor:
                    return 1
                else:
                    return 2
            elif elev_pos == vec.src.floor:
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
            elif elev_pos == vec.src.floor:
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
                elif elev_pos > vec.src.floor:
                    return 3
                else:
                    return 4
                
            else:
                if elev_pos > vec.src.floor:
                    if vec.src.floor>vec.dst.floor:
                        return 1
                    else: 
                        return 2
                elif elev_pos < vec.src.floor:
                    return 3
                else:
                    return 4
                    
    @staticmethod        
    def calc_route_time(vect: list):
        return sum([v.dst.time - v.incoming.time for v in vect])


    def create_basic_course(self, vec:Vector):
        course = []
        course.insert(0,vec.incoming)
        if len(self.call_pointers)>=1:   
            for i in range(len(self.call_pointers)):
                course.append(self.call_pointers[i].incoming)
        return course
    #Can be improved with threads
    def add_vector_to_route(self, vec: Vector, course: list):
        course.insert(0,vec.incoming)
        info = self.get_insertion_index(vec, course)
        for i in range(info[0],info[1]):
            course[i].increase_by_split_cases(self.stop_const.get('full_break'))
        for i in range(info[1]):
            course[i].increase_by_split_cases(self.stop_const.get('full_break'))
        vec.src.time += ceil(info[2])
        vec.dst.time += ceil(info[3])
        course.insert(info[0], vec.src)
        course.insert(info[1], vec.dst)
    
    #start thread in the beginning of and iteration - lock it after 
    # @jit(noPython=True)
    @functools.lru_cache(maxsize=128)
    def create_dummy_course(self, c: Call):
        vec = Vector(c)
        self.add_vector_to_route(vec, self.timed_course)
        self.call_pointers.insert(0,vec)
        self.timed_course.sort(key=lambda x :x.time)
        return self.calc_route_time(self.call_pointers)

    def future_position(self, incoming_node: Node, course: list):
        state = self.get_state(incoming_node, course)
        inc_index = course.index(incoming_node)
        i = inc_index
        pre1 = [node for node in course if node.time< incoming_node.time]
        pre = [node for node in pre1 if node.type != Type.incoming]
        if len(pre) ==0:
            return 0
        last_floor = pre[-1].floor
        if state == 0:
            return last_floor
        next_time = incoming_node.time
        curr_time = course[i].time
        dt = abs(next_time - curr_time)
        dt -= self.stop_const.get("start_course") # Add the time it takes to close the doors and start the elevator
        return last_floor + state * ceil((dt * self.speed_const.get("tpf")))

    #This function calculates the time which take to this call to complete as well as how much delay factor will be caused if we add this call to the list
    def easy_case_same_diretion(self, vec: Vector, course: list):
        pos = self.future_position(vec.incoming, course)
        inc_node, src_node, dst_node = vec.incoming, vec.src, vec.dst
        inc_index = course.index(inc_node)
        src, dst, i, src_delay, dst_delay = src_node.floor, dst_node.floor, inc_index, 0, 0
        inc_index = course.index(inc_node)
        dir = src-pos > 0
        dist = (abs(src-pos)+abs(dst-src))*self.speed_const.get('tpf') + self.stop_const.get('full_break')
        dir = copysign(1, src - pos)
        extra = 0
        if(pos == src):
            extra = self.hard_case_analysis_stop(vec, course) - self.stop_const.get('full_break')
        while i < len(course) and ((dir and course[i].floor >= src_node.floor) or ((not dir) and course[i].floor <= src_node.floor)):
            src_delay += 1
            i += 1
        src_index = i
        src_time = src_delay*(self.stop_const.get('full_break')+extra)+abs(src-pos)*self.speed_const.get('tpf') + self.stop_const.get('end_course')
        while i < len(course) and ((dir and course[i].floor >= dst_node.floor) or ((not dir) and course[i].floor <= dst_node.floor)):
            dst_delay += 1
            i += 1
        dst_index = i
        delay_factor = (2*src_delay +dst_delay)*(self.stop_const.get('full_break')+extra)
        return (src_index, dst_index, src_time , delay_factor + dist)
    
    def easy_case_idle_same_floor(self, vec: Vector, course: list):
        pos = vec.src.floor
        inc_node, src_node, dst_node = vec.incoming, vec.src, vec.dst
        inc_index = course.index(inc_node)
        src, dst, src_delay, dst_delay, i = src_node.floor, dst_node.floor, 0, 0, inc_index
        inc_index = course.index(inc_node)
        dir = src-pos > 0
        extra = 0
        if(pos == src):
            extra = self.hard_case_analysis_stop(vec, course) - self.stop_const.get('full_break')
        while i < len(course) and ((dir and course[i].floor >= dst_node.floor) or ((not dir) and course[i].floor <= dst_node.floor)):
            dst_delay += 1
            i += 1
        dist= (abs(dst-pos))*self.speed_const.get('tpf') + dst_delay*(self.stop_const.get('full_break')+extra)
        return (inc_index, inc_index, 0, dist)

    def easy_case_inverse_direction(self, vec: Vector, course: list):
        pos = self.future_position(vec.incoming, course)
        inc_node, src_node, dst_node = vec.incoming, vec.src, vec.dst
        inc_index = course.index(inc_node)
        src, dst, i, src_delay, dst_delay = src_node.floor, dst_node.floor, inc_index, 0, 0
        inc_index = course.index(inc_node)
        dir = src-pos > 0
        extra = 0
        if(pos == src):
            extra = self.hard_case_analysis_stop(vec, course) - self.stop_const.get('full_break')
        while i < len(course) and ((dir and course[i].floor >= src_node.floor) or ((not dir) and course[i].floor <= src_node.floor)):
            src_delay += 1
            i += 1
        src_index = i
        src_time = src_delay*(self.stop_const.get('full_break')+extra)+abs(src-pos)*self.speed_const.get('tpf') + self.stop_const.get('end_course')
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
        dist += (2*src + dst_delay + 1) * (self.stop_const.get('full_break')+extra)
        return(src_index, dst_index, src_time , dist)

    def hard_case_analysis_stop(self, vec: Vector, course: list):
        pos = self.future_position(vec.incoming, course)
        inc_node, src_node, dst_node = vec.incoming, vec.src, vec.dst
        inc_index = course.index(inc_node)
        src, dst, i, src_delay, dst_delay, state = src_node.floor, dst_node.floor, inc_index, 0, 0, self.get_state(vec.incoming, course)
        relevant1 = [node for node in course if node.time-self.stop_const.get('end_course')<inc_node.time<node.time + self.stop_const.get('start_course')]
        relevant2 = [node for node in relevant1 if node.type != Type.incoming]
        relevant3 = [node for node in relevant2 if node.floor == src_node.floor] 
        relevant4 = []
        loopscount = 0
        if(len(relevant3) == 0):
            return 0
        rel = relevant3[0]
        while len(relevant4) != 0:
            relevant4 = [node for node in relevant3 if node.time < rel.time + self.stop_const.get('start_course')]
            rel = relevant4[-1]
            loopscount += 1
        cmd_delay = ceil(inc_node.time) - ceil(relevant3[0].time)
        delay_by_call = loopscount * self.stop_const.get('full_break') +cmd_delay
        return delay_by_call

        #add cmd_delay to src.time at the end
        
        
    def hard_case_missed_floor(self, vec: Vector, course: list):
        pos = self.future_position(vec.incoming, course)
        inc_node, src_node, dst_node = vec.incoming, vec.src, vec.dst
        inc_index = course.index(inc_node)
        src, dst, i, src_delay, dst_delay = src_node.floor, dst_node.floor, inc_index, 0, 0
        dir = src-pos > 0
        turn1 = self.find_turning_point(i, course)
        src_delay = turn1- i
        i = turn1
        dir = src - pos > 0
        extra = 0
        if(pos == src):
            extra = self.hard_case_analysis_stop(vec, course) - self.stop_const.get('full_break')
        while i < len(course) and ((dir and course[i].floor >= src_node.floor) or ((not dir) and course[i].floor <= src_node.floor)):
            src_delay += 1
            i += 1
        src_index, turn2 = i, self.find_turning_point(i, course)
        dst_delay = turn2 - i
        i = turn2
        while i < len(course) and ((dir and course[i].floor >= dst_node.floor) or ((not dir) and course[i].floor <= dst_node.floor)):
            dst_delay += 1
            i += 1
        dst_index = i
        turn_floor1, turn_floor2 = course[turn1].floor, course[turn2].floor
        src_time =(src_delay*(self.stop_const.get('full_break')+extra)+(abs(turn1-pos)+abs(turn1-src))*self.speed_const.get('tpf')+self.stop_const.get('end_course'))
        dist = (abs(turn_floor1-pos)+abs(turn_floor1-src)+abs(src-turn_floor2)+abs(dst-turn_floor2))*self.speed_const.get('tpf')
        delay_factor = (2*src_delay + dst_delay)*(self.stop_const.get('full_break')+extra)
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
        sign = copysign(1.0, calls[0].floor - calls[1].floor)
        for j in range(1, len(calls)-1):
            s = copysign(1.0, calls[j].floor - calls[j+1].floor)
            if s * sign < 0:
                return i + j + 1
            sign = s
        return -1
    #Can be improved with threads
    def get_state(self, incoming: Node, course: list):
        inc_index = course.index(incoming)
        if inc_index == len(course)-1:
            return Direction.IDLE
        i = inc_index
        # while i-1>0 and course[i].type == Type.incoming:
        #     i -=1
        # last_Stop_floor = course[i].floor
        # j = inc_index
        # while j+1< len(course) and course[j].type == Type.incoming:
        #     j += 1
        pre1 = [node for node in course if node.time< incoming.time]    
        pre = [node for node in pre1 if node.type!= Type.incoming]         
        post1 = [node for node in course if node.time> incoming.time]
        post = [node for node in post1 if node.type != Type.incoming]
        if len(pre)==0 or len(post) ==0:
            return Direction.IDLE 
        next_stop_floor = post[0].floor
        last_stop_floor = pre[-1].floor
        if next_stop_floor > last_stop_floor:
            return Direction.UP
        return Direction.DOWN

    def get_insertion_index(self, vec: Vector, course: list):
        case = self.case_check(vec, course)
        if case == 0:
            dist = (abs(vec.dst.floor-vec.src.floor))*self.speed_const.get('tpf')+self.stop_const.get('full_break')
            tup = (0, 1, vec.incoming.time, dist)
        elif case == 1:
            tup = self.easy_case_same_diretion(vec, course)
        elif case == 2:
            tup = self.easy_case_inverse_direction(vec, course)
        elif case == 3:
            tup = self.hard_case_missed_floor(vec, course)
        elif case == 4:
            tup = self.easy_case_idle_same_floor(vec, course)
        else:
            print("hello")
        return tup
        
    def check_insertion_delay_factor(self, c: Call):
        vec = Vector(c)
        self.timed_course.insert(0,vec.incoming)
        tup = self.get_insertion_index(vec, self.timed_course)
        case = self.case_check(vec, self.timed_course)
        delay_factor = (tup[1]-tup[0])*self.stop_const.get('full_break')+(len(self.timed_course)-1-tup[1])*2*self.stop_const.get('full_break')
        pre = [x for x in self.timed_course if tup[2]-self.stop_const.get('full_break')<tup[2]<tup[2]+self.stop_const.get('full_break')]
        b = [x for x in pre if x == c.src ]
        bb = [x for x in b if x.type != Type.incoming]
        if len(bb)>0:
            delay_factor -= self.stop_const.get('full_break')
        post = [x for x in self.timed_course if tup[2]-self.stop_const.get('full_break')<tup[2]<tup[3]+self.stop_const.get('full_break')]
        a = [x for x in post if x == c.src ]
        aa = [x for x in a if x.type != Type.incoming]
        if len(aa)>0:
            delay_factor -= self.stop_const.get('full_break')
        delay_factor += (tup[3] - vec.incoming.time)
        self.timed_course.remove(vec.incoming)
        return delay_factor

    # def check_if_reach_floor_src(self, vec: Vector):
    #     tup = self.get_insertion_index(vec, self.timed_course)
    #     check = [x for x in self.timed_course if tup[2]-self.stop_const.get('end_course')<=x.time<=tup[2]+self.stop_const.get('start_course')]
    #     find = [x for x in check if ]
