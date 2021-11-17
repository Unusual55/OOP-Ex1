import sys
import json
from Building import Building
from Controller import Controller
from Elevator import Elevator
jsonPath = './data/Ex1_input/Ex1_Buildings/B2.json'
csvPath = './data/Ex1_input/Ex1_Calls/Calls_a.csv'

debuging = True

def main():
    building = Building.parse_from_json(jsonPath)
    controller = Controller.from_csv(csvPath)
    pass


if __name__ == '__main__':
    if debuging:
        main()
        sys.exit(0)
    
    arguments = sys.argv[1:]
    try:
        building_json_path = arguments[0]
    except IndexError:
        raise SystemExit('Please provide a path to a valid json file')
    try:
        calls_csv_path = arguments[1]
    except IndexError:
        raise SystemExit('Please provide a path to a valid csv file')
    try:
        output_file_path = arguments[2]
    except IndexError:
        raise SystemExit('Please provide a path to a valid output file')
    building = Building.parse_from_json(building_json_path)
    calls = Controller.from_csv(calls_csv_path)
    main()
