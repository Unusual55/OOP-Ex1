import sys
import json
from Building import Building

jsonPath = './data/Ex1_input/Ex1_Buildings/B2.json'
# csvPath = './data/Ex1_input/Ex1_Calls/Calls_a.csv'


def main():
    building = Building.parse_from_json(jsonPath)
    print(json.dumps(building, indent=4))
    pass


if __name__ == '__main__':
    main()
