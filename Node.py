from enum import IntEnum
import re
#Enum class that contains the types of Node
class Type(IntEnum):
    incoming = 1
    src = 2
    dst = 3
class Node:
    #This function initialize the Node object
    def __init__(self, id: int, time: float, floor: int, type: int):
        self.id = id
        self.time = time
        self.floor = floor
        self.type = Type(type)
        self.moveable = type != Type.incoming    

    #This function set a connection between src or dst type Node and an incoming node which we
    #get as an input
    def set_conncection_incoming(self, n):
        if self.type != Type.incoming:
            self.incoming = n
    
    #This function set a connection between incoming or dst type Node and an src node which we
    #get as an input
    def  set_connection_src(self, n):
        if self.type != Type.src:
            self.src = n
    
    #This function set a connection between incoming or src type Node and an dst node which we 
    #get as an input
    def set_connection_dst(self, n):
        if self.type != Type.dst:
            self.dst = n
    
    #This function controls the time of a node
    #First, incoming nodes contain the time we recieved the call as it was initialized, and it will
    #not change, so incoming Node moveable property will be false and it's time won't change
    #Second, if we delay the arrival to the source floor, we will delay the arrival to the destenation
    #floor as well, so if the node which we used this function on is a src type, it will increase
    #it's arrival time as well as the time of the dst node it's connected 
    def increase_by_split_cases(self, d: float):
        if self.moveable == False:
            return
        elif self.type == Type.src:
            self.time += d
            self.dst.time += d
        else:
            self.time += d

    #This function get an object as input and check if it's equal to the Node which we used the
    #function on, if the object is Node object, the function will check if all of the fields are
    #equal, if they are it will return True. Otherwise it will return False    
    def __eq__(self, o: object) -> bool:
        if isinstance(o, Node):
            return self.id == o.id and self.time == o.time and self.floor == o.floor and self.type == o.type
        return False
    

