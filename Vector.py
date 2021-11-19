from Node import Node, Type
from Elevator import Elevator
from Call import Call
#Vector is a data structure that contains the 3 types of Nodes for a call, it set up a connection
#between the 3 Nodes and will be used instead of keeping the Call objects.
class Vector:
    #This function initialize the Vector object and set the connection between the 3 Nodes
    def __init__(self, c: Call) -> None:
        self.incoming = Node(c.id, c.time, 0, Type.incoming)
        self.src = Node(c.id, c.time, c.src, Type.src)
        self.dst = Node(c.id, c.time, c.dst, Type.dst)
        self.incoming.set_connection_src(self.src)
        self.incoming.set_connection_dst(self.dst)
        self.src.set_conncection_incoming(self.incoming)
        self.src.set_connection_dst(self.dst)
        self.dst.set_conncection_incoming(self.incoming)
        self.dst.set_connection_src(self.src)
    
    #This function resets the time of the src and dst nodes to their original time- the time of
    #the incoming Node time
    def reset(self):
        self.src.time = self.incoming.time
        self.dst.time = self.incoming.time
