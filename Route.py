from Call import Call
from Node import Node, Type
from Elevator import Direction
from Vector import Vector
import functools
from math import ceil, copysign

#The Route is The course management of the elevator, it's a data structure that contain the list
#of Vector objects that the elevator take care of, a list of Node object which represent it's course
#as well as it's time line for the simulation.
#The Route also contain the important constant we need to take care of during the simulation:
#1. start_course: The time that will take for the elevator to close the doors and start the engine
#2. end_course: The time that will take for the elevator to stop at the wanted floor and open the doors
#3. full_break: The time that will take to stop at wanted floor- the end of the last course and the
#   beginning of a new course
#4. speed: The speed of the elevator, how many floors the elevator pass in 1 second when it's moving
#5. tpf: Time Per Floor- how much time it will take to move 1 floor(1/speed)
class Route:
    #This function initialize the Route object
    def __init__(self, e) -> None:
        import Elevator
        self.call_pointers = []
        self.timed_course = []
        self.stop_const = {'start_course': e.close_time + e.start_time, 'end_course': e.stop_time + e.open_time, 'full_break': e.open_time + e.close_time + e.start_time + e.stop_time}
        self.speed_const = {'speed': e.speed, 'tpf': 1/e.speed}
        self.count = 0
    
    #This function get a vector and a course and check the number of case we need in order to
    #know which case is needed to calculate the index of the src and dst nodes as well as how to
    #calculate the time that will take to finish taking care of the call
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
                    
    #This function get a list of vectors and return the time that will take to finish all of the
    #calls
    @staticmethod        
    def calc_route_time(vect: list):
        return sum([v.dst.time - v.incoming.time for v in vect])

    #This function get a vector create a list that contain only the incoming nodes and return it
    def create_basic_course(self, vec:Vector):
        course = []
        course.insert(0,vec.incoming)
        if len(self.call_pointers)>=1:   
            for i in range(len(self.call_pointers)):
                course.append(self.call_pointers[i].incoming)
        return course
    
    #This function add the vector to the course and update every other node that will be delayed
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
    
    #This function get a Call object, create a vector from it and insert it to the course.
    #Since the add_vector_to_route function update the arrival time of every needed node, the function
    #will sort the timed_course by the times and as a result it will turn it to online-algorithm like
    #course. The function will return the time that will take to finish all of the calls
    @functools.lru_cache(maxsize=128)
    def create_dummy_course(self, c: Call):
        vec = Vector(c)
        self.add_vector_to_route(vec, self.timed_course)
        self.call_pointers.insert(0,vec)
        self.timed_course.sort(key=lambda x :x.time)
        return self.calc_route_time(self.call_pointers)

    #This function calculates the future position of the elevator based on the nodes that already
    #exist in the course
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

    #This function calculates the first easy case when the call and the elevator have the same
    #direction and we can reach the source floor without change the direction
    #The function returns a tuple that contain:
    #1. The index that we need to insert the src node to
    #2. The index that we need to insert the dst node to
    #3. The time that will take to reach the src node
    #4. The time that will take to reach the dst node
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
    
    #This function calculates the second easy case when the elevator is idle and it's position is the
    #same as the src node floor
    #The function returns a tuple that contain:
    #1. The index that we need to insert the src node to
    #2. The index that we need to insert the dst node to
    #3. The time that will take to reach the src node
    #4. The time that will take to reach the dst node
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

    #This function calculates the third easy case when the call and the elevator have different
    #directions but the source floor is in the direction of the elevator.
    #The elevator can reach the source floor, but it will need to change it's direction in order
    #to reach the destenation floor.
    #The function returns a tuple that contain:
    #1. The index that we need to insert the src node to
    #2. The index that we need to insert the dst node to
    #3. The time that will take to reach the src node
    #4. The time that will take to reach the dst node
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

    #This function work as support function for any other cases.
    #We analyzed the simulator and we noticed that an elevator could stuck in a loop inside the same
    #floor if the elevator is at specific position, it was already given an cmd goto command, then
    #if we allocate another call which have the same source floor as the elevator position and the
    #elevator is still at the same floor(didn't finish the time that takes to start a course), then
    #the elevator will finish the start_course time, and then stop at the floor which will take
    #end_course and then start to leave the floor again which will take another start_course.
    #This function check if a situation like this could happen and if it will happed, it returns the
    #extra delay that will be caused because of the loop.
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

    ##This function calculates the first hard case when the call and the elevator have the same
    #direction but we need to change the direction of the elevator in order to reach the source floor
    #and then change it again in order to reach the destenation floor.
    #The function returns a tuple that contain:
    #1. The index that we need to insert the src node to
    #2. The index that we need to insert the dst node to
    #3. The time that will take to reach the src node
    #4. The time that will take to reach the dst node            
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

    #This fuction returns a sorted  of Nodes that sorted by the time property of it's values
    def get_sorted_nodelist(self):
        li = [] 
        for i in self.call_pointers:
            li.append(i[0])
            li.append(i[1])
        return sorted(li, key=lambda x: x.time, reverse=True)

    #This function get an index and a course, and returns the index of the last floor that have the
    #same direction as the elevator, and after it the direction will change
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

    #This function get an incoming Node and a course and return the state of the elevator at the time
    #of the incoming Node
    def get_state(self, incoming: Node, course: list):
        inc_index = course.index(incoming)
        if inc_index == len(course)-1:
            return Direction.IDLE
        i = inc_index
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

    #This function get a vector and a course and return a tuple that returns from the cases calculation
    #function and return it.
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
        else:    
            tup = self.easy_case_idle_same_floor(vec, course)
        return tup
    
    #This function get a call and calculate how much time will take in order to finish taking care
    #of the call and how much delay might be caused to all of the other calls and return a sum
    #of the delay factor and finish time
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
