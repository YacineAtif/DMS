import random
import time
import math
from datetime import datetime  # Assuming get_current_timestamp is replaced with datetime.now()

# Define road characteristics
road_length = 1000  # Length of the road in meters
lanes = [1, 2]  # Two lanes

# Define object types with codes and speed ranges
object_data = {
    "pedestrian": {"code": 0, "speed_range": (1, 5)},
    "bicycle": {"code": 1, "speed_range": (10, 30)},
    "vehicle": {"code": 2, "speed_range": (30, 100)}
}


class TrafficObject:
    def __init__(self, object_id, object_type, lane):
        self.object_id = object_id
        self.object_type = object_type
        self.lane = lane
        speed_range = object_data[object_type]["speed_range"]
        self.speed = random.uniform(*speed_range)
        self.x = 0  # Start at the beginning of the road
        self.y = -10 if lane == 1 else 10  # Assign y based on lane

    def update_position(self):
        # Retrieve the object's speed range from its type
        speed_range = object_data[self.object_type]["speed_range"]

        # Road and lane-specific speed limits could be applied here
        max_speed = 60 if self.lane == 1 else 80  # Example max speeds for different lanes

        # Adjust speed slightly to simulate acceleration/deceleration within the object's speed range and possible road limits
        speed_change = random.uniform(-0.5, 0.5)
        self.speed = max(speed_range[0], min(self.speed + speed_change, min(speed_range[1], max_speed)))

        # Update position considering lane boundaries and forward movement only
        self.x += self.speed / 3600  # Assuming speed is in km/h and time step is 1 second
        # Y-coordinate is not changed since lane changes are not being simulated in this example

    def get_data_row(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        type_code = object_data[self.object_type]["code"]
        return {
            "id": self.object_id,
            "timestamp": timestamp,
            "x": self.x,
            "y": self.y,
            "speed": self.speed,
            "type": type_code,
            "lane": self.lane
        }


# Global variables to manage traffic objects
objects = []
object_counter = 0


def reset_simulation():
    global objects, object_counter
    objects.clear()
    object_counter = 0


def get_simulated_traffic_data(reset=False):
    global object_counter, objects

    if reset:
        reset_simulation()

    if not objects or random.random() < 0.1:
        object_counter += 1
        obj_type = random.choice(list(object_data.keys()))
        lane = random.choice(lanes)
        new_object = TrafficObject(object_counter, obj_type, lane)
        objects.append(new_object)

    for obj in objects:
        obj.update_position()

    return [obj.get_data_row() for obj in objects]  # Return data for all objects


if __name__ == "__main__":
    while True:
        traffic_data = get_simulated_traffic_data()
        for data in traffic_data:
            print(data)
        time.sleep(1)
