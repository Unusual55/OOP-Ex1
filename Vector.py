from Node import Node, Type
from Call import Call

class Vector:
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
    
    def reset(self):
        self.src.time = self.incoming.time
        self.dst.time = self.incoming.time
