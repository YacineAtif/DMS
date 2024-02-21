import random
import time
from Sensors.timestamp_util import get_current_timestamp


# Define standalone functions that can be used independently or within the class
def simulate_driver_state(distraction, drowsiness):
    if random.random() < 0.1:
        drowsiness = min(drowsiness + 1, 4)
    if random.random() < 0.05:
        distraction = 1
    else:
        distraction = 0
    return distraction, drowsiness


def reset_simulation():
    return 0, 0  # Reset distraction and drowsiness


def get_simulated_driver_state_data(reset=False):
    if reset:
        distraction, drowsiness = reset_simulation()
    else:
        distraction, drowsiness = 0, 0  # Initial state
    distraction, drowsiness = simulate_driver_state(distraction, drowsiness)
    timestamp = get_current_timestamp()
    return {
        "timestamp": timestamp,
        "distraction": distraction,
        "drowsiness": drowsiness
    }


class SmartEyeSimulator:
    def __init__(self):
        self.distraction = 0
        self.drowsiness = 0

    def update_state(self):
        self.distraction, self.drowsiness = simulate_driver_state(self.distraction, self.drowsiness)

    def reset_states(self):
        self.distraction, self.drowsiness = reset_simulation()

    def get_data(self):
        # Use the standalone function to simulate driver state data
        data = get_simulated_driver_state_data()
        # Override distraction and drowsiness with the object's current state
        data['distraction'] = self.distraction
        data['drowsiness'] = self.drowsiness
        return data


# Standalone execution
if __name__ == "__main__":
    while True:
        # Example usage for class instance
        driver_simulator = SmartEyeSimulator()
        for _ in range(30):
            driver_simulator.update_state()
            print(driver_simulator.get_data())
            time.sleep(1)

        # Example usage for standalone simulation
        # print("\nStandalone simulation without class instantiation:")
        # for _ in range(30):
        #     print(get_simulated_driver_state_data())
