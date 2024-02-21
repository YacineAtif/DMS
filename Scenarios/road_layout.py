# road_layout.py
class Lane:
    def __init__(self, lane_id, direction):
        self.lane_id = lane_id
        self.direction = direction  # e.g., 'northbound' or 'southbound'
        self.traffic_objects = []  # To hold TrafficObject instances


class RoadLayout:
    def __init__(self, number_of_lanes=2):
        self.lanes = [Lane(lane_id=i, direction='northbound' if i % 2 == 0 else 'southbound') for i in
                      range(number_of_lanes)]

    def add_traffic_object_to_lane(self, traffic_object, lane_id):
        # Assume traffic_object is an instance of TrafficObject
        self.lanes[lane_id].traffic_objects.append(traffic_object)
