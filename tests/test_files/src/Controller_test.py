from Controller import Controller
from Building import Building
from Call import Call
from Elevator import Elevator
import unittest
class Building_test(unittest.TestCase):
    def create_controller_from_csv_test(self):
        c = Controller.from_csv('./test_files/Ex1_Calls_case_2_a.csv')
        self.assertTrue(isinstance(c, Controller))
        for call in c.calls:
            self.assertTrue(isinstance(call, Call))

    def allocate_test(self):
        d = Building.parse_from_json('./test_files/B0_test.json')
        c = Controller.from_csv('./test_files/Ex1_Calls_case_2_a.csv')
        c.allocate(d)
        for call in c.calls:
            self.assertFalse(call.id == -1)
            self.assertEqual(c.allocated_elevators[call.id], call.id)

    if __name__ == "__main__":
        unittest.main()