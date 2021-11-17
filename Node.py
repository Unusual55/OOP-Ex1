from enum import IntEnum

class Type(IntEnum):
    incoming = 1
    src = 2
    dst = 3
class Node:
    def __init__(self, id: int, time: float, floor: int, type: int):
        self.id = id
        self.time = time
        self.floor = floor
        self.type = Type(type)
        self.moveable = type != Type.incoming    

    def set_conncection_incoming(self, n):
        if self.type != Type.incoming:
            self.incoming = n
    
    def  set_connection_src(self, n):
        if self.type != Type.src:
            self.src = n
    
    def set_connection_dst(self, n):
        if self.type != Type.dst:
            self.dst = n
    
    def increase_by_split_cases(self, d: float):
        if self.moveable == False:
            return
        elif self.type == Type.src:
            self.time += d
            self.dst.time += d
        else:
            self.time += d
    

