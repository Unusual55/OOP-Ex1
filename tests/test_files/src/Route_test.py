import unittest
from Node import Node, Type
from Vector import Vector
from Call import Call
from Route import Route
from Elevator import Elevator, Direction
from Call import Call

class Route_test(unittest.TestCase):

    def create_route_test(self):
        e = Elevator(0,1,-2,10,2,2,3,3)
        c1 = Call(1.5, 0, -1, 0)
        c2 = Call(2.5, 0, -1, 2)
        route = Route(e)
        self.assertTrue(isinstance(route,Route))


    if __name__ == "__main__":
        unittest.main()