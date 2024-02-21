# simulation.py
from Sensors.traffic_data import get_simulated_traffic_data, TrafficObject
from road_layout import RoadLayout

# Initialize the road layout
road_layout = RoadLayout()

# Generate traffic data and add objects to lanes
for _ in range(10):  # Simulate adding 10 traffic objects
    traffic_data = get_simulated_traffic_data()
    if traffic_data:
        # Randomly choose a lane for simplicity in this example
        lane_id = 0 if traffic_data['type'] % 2 == 0 else 1
        traffic_object = TrafficObject(**traffic_data)
        road_layout.add_traffic_object_to_lane(traffic_object, lane_id)

# Example to inspect objects in a lane
for lane in road_layout.lanes:
    print(f"Lane {lane.lane_id}, Direction: {lane.direction}")
    for obj in lane.traffic_objects:
        print(f"  - ID: {obj.object_id}, Type: {obj.object_type}, X: {obj.x}, Y: {obj.y}")
