import unittest
from Node import Node, Type
from Vector import Vector
from Call import Call

class Vector_test(unittest.TestCase):

    def create_vector_test(self):
        c: Call(5, 0, 10,0)
        v = Vector(c)
        inc = v.incoming
        src = v.src
        dst = v.dst
        self.assertTrue(isinstance(inc, Node))
        self.assertTrue(isinstance(src, Node))
        self.assertTrue(isinstance(dst, Node))

    def vector_reset(self):
        c: Call(4.32, 0, 10,0)
        v = Vector(c)
        inc = v.incoming
        src = v.src
        dst = v.dst
        src.increase_by_split_cases(25)
        dst.increase_by_split_cases(45)
        self.assertTrue(src.time, 30)
        self.assertTrue(dst.time, 75)
        v.reset()
        self.assertFalse(src.time, 30)
        self.assertFalse(dst.time, 75)
        self.assertTrue(src.time, 5)
        self.assertTrue(dst.time, 5)

    if __name__ == "__main__":
        unittest.main()
