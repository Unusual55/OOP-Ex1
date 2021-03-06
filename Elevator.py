import json
from enum import IntEnum

class Direction(IntEnum):
    IDLE = 0  # When the elevator is idle the doors are open
    UP = 1
    DOWN = -1

class Elevator:
    __elevator_fields = {'_id': 'elevator_id', '_speed': 'speed', '_minFloor': 'min_floor', '_maxFloor': 'max_floor',
                         '_closeTime': 'close_time', '_openTime': 'open_time', '_startTime': 'start_time', '_stopTime': 'stop_time'}

    def __init__(self, elevator_id, speed, min_floor, max_floor, close_time, open_time, start_time, stop_time):
        self.elevator_id = elevator_id
        self.speed = speed  # Floors per second
        self.min_floor = min(min_floor, max_floor)
        self.max_floor = max(min_floor, max_floor)
        self.close_time = close_time
        self.open_time = open_time
        self.start_time = start_time
        self.stop_time = stop_time

        self.position = 0
        self.direction = Direction.IDLE
        import Route
        self.route = Route.Route(self)
    
    def const_time(self):
        return self.close_time + self.open_time + self.start_time + self.stop_time
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.to_json())

    def __str__(self):
        return json.dumps(self, default=lambda o: o.to_json(), indent=4)

    def __repr__(self):
        return str(self.__dict__)

    def to_json(self):
        return {field: getattr(self, att) for field, att in Elevator.__elevator_fields.items()}

    @classmethod
    def parse_elevator(cls, elevator: dict):
        cls.validate_elevator(elevator)
        return cls(**{prop: elevator[jname] for (jname, prop) in cls.__elevator_fields.items()})

    @classmethod
    def validate_elevator(cls, elevator: dict):
        properties = cls.__elevator_fields
        for prop in properties:
            if prop in elevator:
                val = elevator[prop]
                t = type(val)
                if (t != int) and (t != float):
                    raise TypeError(f'{prop} is not a number')
                elif (prop == '_minFloor' or prop == '_maxFloor') and (t == float):
                    raise ValueError(f'{prop} is not an integer')
                if (prop != '_id') and (prop != '_minFloor') and (prop != '_maxFloor'):
                    if val <= 0:
                        if prop == '_speed':
                            raise ValueError(
                                'speed has to be a positive number')
                        raise ValueError(
                            f'{prop} is negative and has to be a non-negative number')

            else:
                raise Exception(f'Elevator property {prop} is missing')
        if elevator['_minFloor'] > elevator['_maxFloor']:
            raise ValueError('The property minFloor is larger maxFloor')
