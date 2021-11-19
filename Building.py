import json
from Elevator import Elevator


class Building:
    #A dictionary with the names of the property of a builing which we need to parse from json files
    __building_fields = {'_minFloor': 'min_floor',
                         '_maxFloor': 'max_floor', '_elevators': 'elevators'}

    #This function initialize the Building object
    def __init__(self, min_floor, max_floor, *elevators):
        self.min_floor = min(min_floor, max_floor)
        self.max_floor = max(min_floor, max_floor)
        self.elevators = [
            elevator for elevator in elevators if isinstance(elevator, Elevator)]
        self.number_of_elevators = len(self.elevators)
        self.number_of_floors = self.max_floor - self.min_floor + 1

    #This function using this building data and write it to .json file
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.to_json())

    #This function using this building data and write it to .json file with indentation
    def __str__(self):
        return json.dumps(self, default=lambda o: o.to_json(), indent=4)

    #This function returns String that represent the data of the building
    def __repr__(self):
        return str(self.__dict__)

    #This function return a dictionary from _building_fields dictionary and replace the value with
    #the real values of this building
    def to_json(self):
        return {field: getattr(self, att) for field, att in Building.__building_fields.items()}

    #This function get a json path, and parse it to a building object
    @classmethod
    def parse_from_json(cls, json_path: str):
        with open(json_path, mode='r') as f:
            buildingDict = json.load(f)
            return cls.parse_building(buildingDict)

    #This function get a dictionary of field which Building object contain, check if the input is
    #valid: if the input is invalid, it will raise an exception, otherwise it will parse it to
    #Building object using the dictionary's values
    @classmethod
    def parse_building(cls, building: dict):
        cls.validate_building(building)
        return cls(building['_minFloor'], building['_maxFloor'],  *[Elevator.parse_elevator(elevator) for elevator in building['_elevators']])

    #This function get a dictionary that contain the fields of a building in order to check if the
    #input is valid, if it's invalid, the function will raise an exception.
    @classmethod
    def validate_building(cls, building: dict):
        properties = cls.__building_fields
        for prop in properties:
            if prop in building:
                val = building[prop]
                t = type(val)
                if prop == '_elevators':
                    if t != list:
                        raise TypeError('_elevators is not a list')
                    if len(val) == 0:
                        raise ValueError('_elevators is empty')
                else:
                    if t != int:
                        raise TypeError(f'{prop} is not an integer')
            else:
                raise Exception(f'Building property {prop} is missing')
        for elevator in building['_elevators']:
            Elevator.validate_elevator(elevator)
            if (elevator['_maxFloor'] != building['_maxFloor']) or (elevator['_minFloor'] != building['_minFloor']):
                raise Exception(
                    'Elevator floor range does not match building floor range')
