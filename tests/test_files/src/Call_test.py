import unittest
from Call import Call
class Call_test(unittest.TestCase):

    def create_call(self):
        c = Call(2.36, 0, 12, 0)
        self.assertTrue(isinstance(c, Call))

    if __name__ == "__main__":
        unittest.main()