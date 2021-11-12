class Elevator:
    __elevator_fields = ['_id', '_speed', '_minFloor', '_maxFloor',
                         '_closeTime', '_openTime', '_startTime', '_stopTime']

    def __init__(self, elevator_id, speed, min_floor, max_floor, close_time, open_time, start_time, stop_time):
        self.elevator_id = elevator_id
        self.speed = speed
        self.min_floor = min(min_floor, max_floor)
        self.max_floor = max(min_floor, max_floor)
        self.close_time = close_time
        self.open_time = open_time
        self.start_time = start_time
        self.stop_time = stop_time

    @staticmethod
    def parse_elevator(elevator: dict):
        Elevator.validate_elevator(elevator)
        return Elevator(**[elevator[prop] for prop in Elevator.__elevator_fields])

    @staticmethod
    def validate_elevator(elevator: dict):
        properties = Elevator.__elevator_fields
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
