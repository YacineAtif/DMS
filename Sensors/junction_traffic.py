import random
import time

# Define vehicle data
vehicle_data = {
    "vehicle": {"code": 2, "speed_range": (30, 100)}  # Speed in km/h
}

object_id_counter = 1  # Global counter for vehicle IDs, starting from 1

class VehicleObject:
    def __init__(self, object_id, road_direction):
        global object_id_counter

        self.object_id = object_id
        self.object_type = "vehicle"
        self.road_direction = road_direction  # Initial direction: 'north', 'south', 'east', 'west'
        self.next_direction = self.determine_next_direction()  # Determine the next direction at the junction

        speed_range = vehicle_data[self.object_type]["speed_range"]
        self.speed = random.uniform(*speed_range)  # Initial speed

        # Start position along each lane, randomly positioned close to the edge
        lane_start_positions = {
            'north': (0, random.uniform(50, 100)),
            'south': (0, random.uniform(-100, -50)),
            'east': (random.uniform(-100, -50), 0),
            'west': (random.uniform(50, 100), 0)
        }
        self.x, self.y = lane_start_positions[road_direction]

        object_id_counter += 1

    def determine_next_direction(self):
        # Possible directions a vehicle can take at the junction based on its initial direction
        direction_options = {
            'north': ['north', 'west', 'east'],
            'south': ['south', 'west', 'east'],
            'east': ['east', 'north', 'south'],
            'west': ['west', 'north', 'south']
        }
        return random.choice(direction_options[self.road_direction])

    def update_position(self):
        distance = self.speed / 3600  # Convert speed to km/s for 1 second

        # Update position based on the current direction, adjust at junction if necessary
        if self.road_direction == 'north' and self.y < 0 or self.road_direction == 'south' and self.y > 0:
            self.y += distance if self.road_direction == 'north' else -distance
        elif self.road_direction == 'east' and self.x < 0 or self.road_direction == 'west' and self.x > 0:
            self.x += distance if self.road_direction == 'east' else -distance
        # Handle turns at the junction based on next_direction
        else:
            if self.next_direction == 'north':
                self.y += distance
            elif self.next_direction == 'south':
                self.y -= distance
            elif self.next_direction == 'east':
                self.x += distance
            elif self.next_direction == 'west':
                self.x -= distance

    def get_data(self):
        return {
            "id": self.object_id,
            "type": self.object_type,
            "x": round(self.x, 2),
            "y": round(self.y, 2),
            "speed": self.speed,
            "direction": self.next_direction  # Show the next direction after the junction
        }

vehicles = []

def simulate_traffic(initial_vehicle_count=10):
    global vehicles, object_id_counter
    for _ in range(initial_vehicle_count):
        road_direction = random.choice(['north', 'south', 'east', 'west'])
        vehicle = VehicleObject(object_id_counter, road_direction)
        vehicles.append(vehicle)

def update_and_print_vehicle_positions():
    for vehicle in vehicles:
        vehicle.update_position()
        print(vehicle.get_data())

if __name__ == "__main__":
    simulate_traffic()
    try:
        for _ in range(30):  # Simulate for 30 seconds
            update_and_print_vehicle_positions()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Simulation ended.")
