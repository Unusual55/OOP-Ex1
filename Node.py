import Node
class Node:
    def __init__(self, id: int, time: float, floor: int, type: bool):
        self.id = id
        self.time = time
        self.floor = floor
        self.type = type
        self.connect_to = None

    #A function which will be called after the constructor in order to have pointer from one Node to it's pair - point from src to dest and from dest to src
    def set_pair(self, n2: Node.Node):
        self.connect_to = n2
    
    def id(self):
        return self.id
    
    def time(self):
        return self.time

    def floor(self):
        return self.floor
    
    def type(self):
        return self.type
