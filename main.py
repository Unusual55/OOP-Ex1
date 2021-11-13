import sys
import json
from Building import Building
from Elevator import Elevator
jsonPath = './data/Ex1_input/Ex1_Buildings/B2.json'
# csvPath = './data/Ex1_input/Ex1_Calls/Calls_a.csv'


def main():
    building = Building.parse_from_json(jsonPath)
    pass


if __name__ == '__main__':
    main()
