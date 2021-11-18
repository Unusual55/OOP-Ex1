import unittest
from Node import Node, Type
class Node_test(unittest.TestCase):
    def create_node_test(self):
        a = Node(0, 1.5, 1, 1)
        b = Node(0, 1.5, 1, 1)
        c = Node(0, 1.5, 1, 1)
        self.assertTrue(a.type,Type.incoming)
        self.assertTrue(b.type,Type.src)
        self.assertTrue(c.type,Type.dst)
        a.set_connection_src(b)
        self.assertTrue(a.src, b)
        a.set_connection_dst(c)
        b.set_conncection_incoming(a)
        b.set_connection_dst(c)
        c.set_conncection_incoming(a)
        c.set_connection_src(b)
        self.assertTrue(b.dst, c)
        self.assertTrue(c.incoming, a)

    def pushed_by_delay_test(self):
        a = Node(0, 1.5, 1, 1)
        b = Node(0, 1.5, 1, 1)
        c = Node(0, 1.5, 1, 1)
        a.set_connection_src(b)
        a.set_connection_dst(c)
        b.set_conncection_incoming(a)
        b.set_connection_dst(c)
        c.set_conncection_incoming(a)
        c.set_connection_src(b)
        a.increase_by_split_cases(5)
        self.assertFalse(a.time, 6.5)
        b.increase_by_split_cases(5)
        self.assertTrue(b.time, 6.5)
        self.assertTrue(c.time, 6.5)
        c.increase_by_split_cases(5)
        self.assertFalse(b.time, 11.5)
        self.assertTrue(c.time, 11.5)

    def equal_nodes(self):
        a = Node(0, 1.5, 1, 1)
        b = Node(0, 1.5, 1, 1)
        c = Node(0, 1.5, 1, 1)
        a.set_connection_src(b)
        a.set_connection_dst(c)
        b.set_conncection_incoming(a)
        b.set_connection_dst(c)
        c.set_conncection_incoming(a)
        c.set_connection_src(b)
        a.increase_by_split_cases(5)
        d = Node(0, 1.5, 1, 1)
        self.assertFalse(a.__eq__(d))
        d.set_connection_src(b)
        d.set_connection_dst(c)
        self.assertTrue(a.__eq__(d))

        



    if __name__ == "__main__":
        unittest.main()
