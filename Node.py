from Node import Node
from enum import Enum
class Type(Enum):
    incoming = 1
    src = 2
    dst = 3
class Node:
    def __init__(self, id: int, time: float, floor: int, type: int):
        self.id = id
        self.time = time
        self.floor = floor
        self.type = 0
        self.moveable = True
        if type == 1:
            self.type = Type.incoming
            self.moveable = False
        elif type == 2:
            self.type = Type.src
        else:
            self.type = Type.dst        

    def set_conncection_incoming(self, n:Node):
        if self.type == Type.incoming:
            return
        self.incoming = n
    
    def  set_connection_src(self, n: Node):
        if self.type == Type.src:
            return
        self.src = n
    
    def set_connection_dst(self, n: Node):
        if self.type == Type.dst:
            return
        self.dst = n
    
    def time(self):
        return self.time

    def floor(self):
        return self.floor
    
    def type(self):
        return self.type

    def increase_by_split_cases(self, d: float):
        if self.moveable == False:
            return
        elif(self.type == Type.src):
            self.time += d
            self.dst.time += d
        else:
            self.time += d
    

