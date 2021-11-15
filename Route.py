from typing import Tuple
import Call, Elevator, Node, copy
class Route:
    def __init__(self, e: Elevator.Elevator) -> None:
        self.call_pointers = [Node.Node, Node.Node]
        self.timed_course = [Node.Node]
        self.stop_const = {'start_course': e.close_time + e.start_time, 'end_course': e.stop_time + e.open_time, 'full_break': e.open_time + e.close_time + e.start_time + e.stop_time}
        self.speed_const = {'speed': e.speed, 'tpf': 1/e.speed}
        self.count = 0
        
    
    def create_vector_node(self, c: Call.Call):
        v1 = Node.Node(c.id, c.time, c.src, True)
        v2 = Node.Node(c.id, 0, c.dst, False)
        v1.set_pair(v2)
        v2.set_pair(v1)
        #calculate time to finish
        vector = [v1, v2]
        #self.call_pointers.insert(0, vector)
        #not finished, need another support functions
        return vector
    
    def add_vector_to_route(self, c: Call.Call):
        pass

    def Route_Offer(self, c: Call.Call):
        pass

    def route_optimal_now(self):
        pass

    @staticmethod
    def reroute(course: list[Node.Node]):
        pass

    #This function calculates the time which take to this call to complete as well as how much delay factor will be caused if we add this call to the list
   # def easy_case_same_direction_pickup_time_calc(self, vector: list[Node.Node,Node.Node], pos: int):
        # srcnode = vector[0]
        # dstnode = vector[1]
        # srcindex = self.timed_course.index(vector[0])
        # dstindex = self.timed_course.index(vector[1])
        # stop_count = (dstindex-srcindex)* self.speed_const.get('full_break')
        # checker = dstindex + 1
        # while dstnode.time< self.timed_course[checker].time:
        #     checker+=1
        # stop_count += 2*self.speed_const.get('full_break')
        # distance = (abs(srcnode.floor-pos)+abs(dstnode.floor-srcnode.floor))*self.speed_const.get('tpf')
        # link = self.stop_const.get('full_break')
        # return stop_count + distance + link

    
    def easy_case_same_inverse_direction_pickup_time_calc(self, vector: list[Node.Node, Node.Node]):
        pass

    def hard_case_missed_floor_time_calc(self, vector: list[Node.Node, Node.Node]):
        pass

    def get_sorted_nodelist(self):
        li = [] 
        for i in self.call_pointers:
            li.append(i[0])
            li.append(i[1])
        return sorted(li, key=lambda x: x.time, reverse=True)

    def find_turning_point(self, i: int):
        pass

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


    
    