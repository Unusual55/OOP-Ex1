import json
from Elevator import Elevator


class Building:
    __building_fields = {'_minFloor': 'min_floor',
                         '_maxFloor': 'max_floor', '_elevators': 'elevators'}

    def __init__(self, min_floor, max_floor, *elevators):
        self.min_floor = min(min_floor, max_floor)
        self.max_floor = max(min_floor, max_floor)
        self.elevators = [
            elevator for elevator in elevators if isinstance(elevator, Elevator)]
        self.number_of_elevators = len(self.elevators)
        self.number_of_floors = self.max_floor - self.min_floor + 1

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.to_json())

    def __str__(self):
        return json.dumps(self, default=lambda o: o.to_json(), indent=4)

    def __repr__(self):
        return str(self.__dict__)

    def to_json(self):
        return {field: getattr(self, att) for field, att in Building.__building_fields.items()}

    @classmethod
    def parse_from_json(cls, json_path: str):
        with open(json_path, mode='r') as f:
            buildingDict = json.load(f)
            return cls.parse_building(buildingDict)

    @classmethod
    def parse_building(cls, building: dict):
        cls.validate_building(building)
        return cls(building['_minFloor'], building['_maxFloor'],  *[Elevator.parse_elevator(elevator) for elevator in building['_elevators']])

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
