import carla
import random


# Simulate distraction and drowsiness
def simulate_driver_state(vehicle, distraction_level, drowsiness_level):
    control = vehicle.get_control()

    # Adjust control based on distraction
    if distraction_level > 0:
        control.steer += random.uniform(-0.1, 0.1) * distraction_level  # Simulate erratic steering
        control.throttle *= (1 - 0.1 * distraction_level)  # Simulate reduced attention to throttle

    # Adjust control based on drowsiness level
    if drowsiness_level > 0:
        control.steer += random.uniform(-0.05, 0.05) * drowsiness_level  # Simulate drifting
        if random.random() < 0.05 * drowsiness_level:
            control.brake = 0.5  # Simulate sudden braking

    # Apply the adjusted control to the vehicle
    vehicle.apply_control(control)


# Create a Carla object
client = carla.Client('localhost', 2000)

# Set a timeout for network operations between the client and the CARLA serve
client.set_timeout(10.0)  # seconds

# Retrieves the  world world object representing the simulation environment
# in CARLA, including all the actors (e.g. vehicles, bikes and pedestrians),
# the map, weather conditions, etc.
world = client.get_world()

# Get Carla tempaltes for the world object including for e.g.specific car models
blueprint_library = world.get_blueprint_library()

# Get Simulated traffic objects
# Example simulated traffic objects
simulated_traffic_objects = [
    {'type': 'vehicle', 'x': 100, 'y': 200}
    # Add more objects
]

# Make Carla actors from simulated traffic object
for traffic_object in simulated_traffic_objects:
    if traffic_object['type'] == 'vehicle':
        # Select a random vehicle
        vehicle_bp = random.choice(blueprint_library.filter('vehicle'))
        # Get Carla position point from traffic object coordinates
        spawn_point = carla.Transform(carla.Location(x=traffic_object['x'], y=traffic_object['y']),
                                      carla.Rotation(0, 0, 0))
        # Position actor on Carla map
        vehicle = world.spawn_actor(vehicle_bp, spawn_point)
        # Set the vehicle's speed
        vehicle.set_target_velocity(carla.Vector3D(traffic_object['speed'], 0, 0))

# Create ego vehicle with driver states converted into vehicle behaviour
# Level of distraction results in erratic steering, or sudden changes in speed.
# Drowsiness leads to drifting between lanes or inconsistent braking
# Example settings for distraction and drowsiness
distraction = 1
drowsiness_level = 3

# Apply simulated driver state to the vehicle
simulate_driver_state(vehicle, distraction, drowsiness_level)
