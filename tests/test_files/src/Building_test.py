import unittest
from Building import Building
from Elevator import Elevator
class Building_test(unittest.TestCase):

    def create_building_test(self):
        e0 = Elevator(0,1,-2,10,2,2,3,3)
        e1= Elevator(1,2,-2,10,2,2,3,3)
        e2 = Elevator(2,3,-2,10,2,2,3,3)
        e3 = Elevator(3,2,-2,10,2,2,3,3)
        e4 = Elevator(4,1,-2,10,2,2,3,3)
        b = Building(-2, 10, e0, e1, e2, e3, e4)
        self.assertTrue(b, Building)

    def parse_from_json_test(self):
        d = Building.parse_from_json('./test_files/B0_test.json')
        self.assertTrue(isinstance(d, dict))

    def parse_building_test(self):
        d = Building.parse_from_json('./test_files/B0_test.json')
        b = Building.parse_building(d)
        self.assertTrue(isinstance(b, Building))

    def validate_building_test(self):
        d = Building.parse_from_json('./test_files/BMinus1_test.json')
        self.assertRaises(Building.parse_building(d))

    if __name__ == "__main__":
        unittest.main()