import sys
import json
from BuildingParser import BuildingParser

jsonPath = './data/Ex1_input/Ex1_Buildings/B2.json'
# csvPath = './data/Ex1_input/Ex1_Calls/Calls_a.csv'


def main():
    parser = BuildingParser(jsonPath)
    print(json.dumps(parser.building, indent=4))
    pass


if __name__ == '__main__':
    main()
