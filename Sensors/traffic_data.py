import random
import time
import math
from Sensors.timestamp_util import get_current_timestamp


# Define a mapping for object types to numerical codes and their typical speed ranges
object_data = {
    "pedestrian": {"code": 0, "speed_range": (1, 5)},
    "bicycle": {"code": 1, "speed_range": (10, 30)},
    "vehicle": {"code": 2, "speed_range": (30, 100)}
}


class TrafficObject:
    def __init__(self, object_id, object_type):
        self.object_id = object_id
        self.object_type = object_type
        speed_range = object_data[object_type]["speed_range"]
        self.speed = random.uniform(*speed_range)  # Initial speed based on object type
        self.x = random.uniform(-100, 100)  # Initial X-coordinate
        self.y = random.uniform(-100, 100)  # Initial Y-coordinate

    def update_position(self):
        # Adjust speed slightly to simulate acceleration/deceleration within the object's speed range
        speed_range = object_data[self.object_type]["speed_range"]
        speed_change = random.uniform(-0.5, 0.5)
        self.speed = max(speed_range[0], min(self.speed + speed_change, speed_range[1]))

        # Update position based on speed, different types of objects will have different movement patterns
        angle = random.uniform(0, 360)  # Random angle for direction
        radian = math.radians(angle)
        distance = self.speed / 3600  # Convert speed to km/s
        self.x += math.cos(radian) * distance
        self.y += math.sin(radian) * distance

    def get_data_row(self):
        timestamp = get_current_timestamp()
        type_code = object_data[self.object_type]["code"]
        # Return formatted data row
        return {
            "id": self.object_id,
            "timestamp": timestamp,
            "x": self.x,
            "y": self.y,
            "speed": self.speed,
            "type": type_code
        }


# Global variables to keep track of objects and IDs
objects = []
object_counter = 0
object_types = list(object_data.keys())


def reset_simulation():
    global objects, object_counter
    objects = []
    object_counter = 0


def get_simulated_traffic_data(reset=False):
    global object_counter, objects

    # Reset the simulation if required
    if reset:
        reset_simulation()

    # Randomly add new objects or update existing ones
    if not objects or random.random() < 0.1:
        object_counter += 1
        obj_type = random.choice(object_types)
        new_object = TrafficObject(object_counter, obj_type)
        objects.append(new_object)

    # Update position of all objects
    for obj in objects:
        obj.update_position()

    # Yield the traffic data row by row (for the last object for this example)
    return objects[-1].get_data_row() if objects else None


# Standalone execution
if __name__ == "__main__":
    while True:
        traffic_data = get_simulated_traffic_data()
        if traffic_data:
            print(traffic_data)
        time.sleep(1)  # Each iteration represents one second
