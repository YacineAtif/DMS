import random
import time
from Sensors.timestamp_util import get_current_timestamp


class SmartEyeSimulator:
    def __init__(self):
        self.distraction = 0
        self.drowsiness = 0

    def update_state(self):
        # Simulate changes in distraction and drowsiness
        if random.random() < 0.1:
            self.drowsiness = min(self.drowsiness + 1, 4)
        if random.random() < 0.05:
            self.distraction = 1
        else:
            self.distraction = 0

    def reset_states(self):
        # Reset distraction and drowsiness to initial states
        self.distraction = 0
        self.drowsiness = 0

    def get_data(self):
        # Return the current state along with a timestamp
        timestamp = get_current_timestamp()
        return {
            "timestamp": timestamp,
            "distraction": self.distraction,
            "drowsiness": self.drowsiness
        }


# Instantiate the simulator globally
driver_simulator = SmartEyeSimulator()


def get_updated_driver_state_data(reset=False):
    # Update or reset the driver's state based on the reset flag
    if reset:
        driver_simulator.reset_states()
    else:
        driver_simulator.update_state()
    return driver_simulator.get_data()


# Standalone execution
if __name__ == "__main__":
    for _ in range(30):
        # Simulate and print driver state data
        print(get_updated_driver_state_data())
        time.sleep(1)
    # Example of resetting the simulation
    print("\nResetting simulation...\n")
    print(get_updated_driver_state_data(reset=True))
