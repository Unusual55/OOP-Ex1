import json


class BuildingParser:
    __buildingProperties = ['_minFloor', '_maxFloor', '_elevators']
    __elevatorProperties = ['_id', '_speed', '_minFloor', '_maxFloor',
                            '_closeTime', '_openTime', '_startTime', '_stopTime']

    def __init__(self, jsonPath):
        with open(jsonPath) as jsonFile:
            buildingDict = json.load(jsonFile)
            self.building = self.parseBuilding(buildingDict)
        pass

    def __parseElevator(self, elevator):
        elevatorDict = {}
        for prop in BuildingParser.__elevatorProperties:
            elevatorDict[prop] = elevator[prop]
        return elevatorDict

    def parseBuilding(self, building):
        BuildingParser.validateBuilding(building)
        buildingDict = {}
        for prop in BuildingParser.__buildingProperties:
            value = building[prop]
            if prop != '_elevators':
                buildingDict[prop] = value
            else:
                buildingDict[prop] = [self.__parseElevator(
                    elevator) for elevator in value]
        return buildingDict

    @staticmethod
    def validateBuilding(building: dict):
        # properties = ['_minFloor', '_maxFloor', '_elevators']
        properties = BuildingParser.__buildingProperties
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
            BuildingParser.validateElevator(elevator)
            if (elevator['_maxFloor'] != building['_maxFloor']) or (elevator['_minFloor'] != building['_minFloor']):
                raise Exception(
                    'Elevator floor range does not match building floor range')

    @staticmethod
    def validateElevator(elevator: dict):
        # properties = ['_id', '_speed', '_minFloor', '_maxFloor', '_closeTime', '_openTime', '_startTime', '_stopTime']
        properties = BuildingParser.__elevatorProperties
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
