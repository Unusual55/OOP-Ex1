from Node import Node, Type
from Elevator import Elevator
from Call import Call
class Vector:
    def __init__(self, c: Call) -> None:
        self.nodes = []
        v1 = Node(c.id, c.time, 0, 1)
        v2 = Node(c.id, -1, c.src, 2)
        v3 = Node(c.id, -1, c.dst, 3)
        v1.set_connection_src(v2)
        v1.set_connection_dst(v3)
        v2.set_conncection_incoming(v1)
        v2.set_connection_dst(v3)
        v3.set_conncection_incoming(v1)
        v3.set_connection_src(v2)
        self.nodes.append(v1)
        self.nodes.append(v2)
        self.nodes.append(v3)
    
    def reset(self):
        self.nodes[1].time = -1
        self.nodes[2].time = -1
        self.nodes[1].next = None
        self.nodes[2].next = None
        self.nodes[0].next = None
