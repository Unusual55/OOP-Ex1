import unittest
from Elevator import Elevator, Direction
from Route import Route
from Building import Building
class Elevator_test(unittest.TestCase):

    def create_elevator_test(self):
         e = Elevator(0,1,-2,10,2,2,3,3)
         self.assertTrue(e, Elevator)
         self.assertTrue(e.route, Route)

    def parse_from_json_test(self):
        d = Building.parse_from_json('./test_files/B0_test.json')
        for i in range(d.number_of_elevators):
            self.assertFalse(self.assertRaises(Elevator.validate_elevator(d.elevators[i].to_json)))
            self.assertTrue(isinstance(d.elevators[i], Elevator))


    if __name__ == "__main__":
        unittest.main()