import sys
from Building import Building
from Controller import Controller

if __name__ == '__main__':
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
    
    calls.allocate(building)
    calls.to_csv(output_file_path)
