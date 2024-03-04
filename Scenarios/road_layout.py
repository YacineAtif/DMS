class Lane:
    def __init__(self, lane_id, direction):
        self.lane_id = lane_id
        self.direction = direction  # 'north', 'south', 'east', 'west'
        self.traffic_objects = []  # Placeholder for TrafficObject instances


class Road:
    def __init__(self, road_id, directions):
        self.road_id = road_id
        # Initialize lanes with specified directions
        self.lanes = [Lane(lane_id=i, direction=direction) for i, direction in enumerate(directions)]


class Junction:
    def __init__(self, junction_id):
        self.junction_id = junction_id
        self.connected_roads = []  # List to hold connected Road instances

    def connect_road(self, road):
        self.connected_roads.append(road)

    def visualize_junction(self):
        print(f"Junction {self.junction_id} connects the following roads and lanes:")
        for road in self.connected_roads:
            lanes = ", ".join([lane.direction for lane in road.lanes])
            print(f"  Road {road.road_id} with lanes: {lanes}")

        # Detailed textual visualization matches the direction of lanes as described
        print("\nTextual Road Layout Visualization:")
        print("        ↓ ↑        ")  # Southbound and northbound lanes
        print("        ↓ ↑        ")  # Further emphasizing southbound and northbound direction
        print("        ↓ ↑        ")  # Further emphasizing southbound and northbound direction
        print("← ← ← ← ← ← ← ← ← ←")  # East to west lane
        print("→ → → → → → → → → →")  # West to east lane
        print("        ↓ ↑        ")  # Southbound and northbound lanes again for symmetry
        print("        ↓ ↑        ")  # Further emphasizing southbound and northbound direction
        print("        ↓ ↑        ")  # Further emphasizing southbound and northbound direction


def setup_road_layout():
    # Create two roads, each with lanes for both directions
    road1 = Road(road_id=1, directions=['south', 'north'])  # South-north road
    road2 = Road(road_id=2, directions=['west', 'east'])  # West-east road

    # Create a junction and connect both roads to it
    junction = Junction(junction_id=0)
    junction.connect_road(road1)
    junction.connect_road(road2)

    return junction


def main():
    # Set up the road layout
    junction = setup_road_layout()

    # Visualize the junction to verify the setup
    junction.visualize_junction()


if __name__ == "__main__":
    main()
