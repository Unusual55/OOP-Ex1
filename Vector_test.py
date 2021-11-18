import unittest
from Node import Node, Type
from Vector import Vector
from Call import Call

class Vector_test(unittest.TestCase):

    def create_vector_test(self):
        c: Call(4.32, 0, 10,0)
        v = Vector(c)
        inc = v.incoming
        src = v.src
        dst = v.dst
        self.assertTrue(isinstance(inc, Node))
        self.assertTrue(isinstance(src, Node))
        self.assertTrue(isinstance(dst, Node))


    if __name__ == "__main__":
        unittest.main()
