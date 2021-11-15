class Route:
    def __init__(self, *stops):
        self.stops = [c for c in stops]
        self.distances = Route.calc_distances(self.stops)
    
    def add(self, stop):
        self.stops.insert(self.minimal_distance_index(stop), stop)
        self.distances = Route.calc_distances(self.stops)
        
    @staticmethod
    def calc_distances(stops):
        return [abs(next - prev) for prev, next in zip(stops, stops[1:])]
    
    def total_distance(self):
        return sum(self.distances)
    
    # TODO: We don't consider if the stop already exists in the stops list, this could cause problems since the elevator would have the floor multiple times
    def minimal_distance_index(self, stop):
        if len(self) == 0:
            return 0
        stops = self.stops.copy()
        dists = [sum(Route.calc_distances(stops[:i] + [stop] + stops[i:])) for i in range(len(stops)+1)]
        return dists.index(min(dists))
    
    
    def __getitem__(self, index):
        return self.stops[index]
    
    def __len__(self):
        return len(self.stops)
    
    