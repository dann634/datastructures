import random

from matplotlib import pyplot as plt

from AlgorithmEnum import Algorithm
from LiftManager import LiftManager
from Call import Call

#STANDARD CONSTANTS FOR TESTING
DEFAULT_MIN_PEOPLE = 5
DEFAULT_MAX_PEOPLE = 2000
DEFAULT_PEOPLE_STEP = 5
DEFAULT_LIFT_CAPACITY = 12
DEFAULT_IGNORE_WEIGHT = False
DEFAULT_FLOORS = 30
DEFAULT_USE_PRIORITY = True


def file_testing(filename : str,
                 algorithm : Algorithm,
                 start_floor : int,
                 start_direction : str):

    print("*" * 40)
    print(f"TEST USING {algorithm} WITH FILE {filename}")
    print("*" * 40)
    print()

    with open(f"input_files/{filename}", "r") as file:
        file_lines = file.readlines()
        file.close()

    num_floors, min_floor, lift_capacity = file_lines[1].split(",")
    num_floors = int(num_floors.strip())
    min_floor = int(min_floor.strip())
    max_floor = min_floor + num_floors - 1
    lift_capacity = int(lift_capacity.strip())

    floor_requests = {}
    for file_line in file_lines[3:]:
        requests = []
        floor, requests_on_floor = file_line.split(":")
        requests_on_floor = requests_on_floor.strip()

        if requests_on_floor != "":
            floor = int(floor.strip())
            for request in requests_on_floor.split(","):
                requests.append(int(request))
                floor_requests[floor] = requests

    people_served = 0
    lift_manager = LiftManager(
        algorithm=algorithm,
        capacity=lift_capacity,
        direction=start_direction,
        current_floor=start_floor,
        floors=num_floors,
        ignore_weight=DEFAULT_IGNORE_WEIGHT,
        use_priority_queue=DEFAULT_USE_PRIORITY
    )

    while floor_requests:
        people_served = people_served + 1
        random.seed(None)
        external_floor_request = random.choice(list(floor_requests.keys()))
        lift_manager.lift_queue.enqueue(Call(external_floor_request, False))

        internal_floor_request = floor_requests[external_floor_request][0]
        lift_manager.lift_queue.enqueue(Call(internal_floor_request, True))

        floor_requests[external_floor_request].pop(0)

        if len(floor_requests[external_floor_request]) < 1:
            del floor_requests[external_floor_request]

    floors_traversed = 0
    total_floors_traversed = 0

    for x in range(lift_manager.lift_queue.size()):
        start_floor = lift_manager.current_floor
        next_floor = lift_manager.process_next_request()
        lift_manager.current_floor = next_floor

        if algorithm == Algorithm.SCAN and lift_manager.reached_limit:
            if lift_manager.current_direction == "up":
                floors_traversed = (start_floor - min_floor) + (lift_manager.current_floor - min_floor)
            elif lift_manager.current_direction == "down":
                floors_traversed = (max_floor - start_floor) + (max_floor - lift_manager.current_floor)

        else:
            floors_traversed = abs(start_floor - lift_manager.current_floor)

        total_floors_traversed = total_floors_traversed + floors_traversed
        print(f"The lift has traveled from floor {start_floor} to floor {lift_manager.current_floor}. It has traversed {floors_traversed} floor(s).")

    print()
    print(f"The lift traveled a total of {total_floors_traversed} floor(s) when serving {people_served} people.")
    return floor_requests, people_served


"""
RANDOM_TESTING
"""
def random_testing(
        algorithm : Algorithm,
        number_of_people=DEFAULT_MAX_PEOPLE,
        lift_capacity=DEFAULT_LIFT_CAPACITY,
        ignore_weight=DEFAULT_IGNORE_WEIGHT,
        use_priority=DEFAULT_USE_PRIORITY
):


    # Lift Variables
    floors = DEFAULT_FLOORS

    # People lists
    people = []
    lift_people = []

    # Tracking metrics
    total_floors_travelled = 0

    lift_manager = LiftManager(
        algorithm=algorithm,
        capacity=lift_capacity,
        direction="up",
        current_floor=0,
        floors=floors,
        ignore_weight=ignore_weight,
        use_priority_queue=use_priority
    )


    for _ in range(number_of_people):
        starting_floor = random.randint(0, floors)
        lift_manager.lift_queue.enqueue(Call(starting_floor, False))
        people.append(starting_floor)

    while len(people) > 0 or len(lift_people) > 0:
        # Run the loop
        next_floor = lift_manager.process_next_request()

        if lift_manager.reached_limit:
            floors_traversed = 0
            if lift_manager.current_direction == "up":
                floors_traversed = (floors - lift_manager.current_floor) + (floors - next_floor)
            elif lift_manager.current_direction == "down":
                floors_traversed = lift_manager.current_floor + next_floor

            total_floors_travelled += floors_traversed

        if not lift_manager.reached_limit:
            total_floors_travelled += abs(next_floor - lift_manager.current_floor)
        lift_manager.current_floor = next_floor

        # Check if anyone needs to get out
        requests_to_remove = []
        for request in lift_people:
            if request == lift_manager.current_floor:
                # this is your floor
                lift_manager.remove_person()
                requests_to_remove.append(request)

        for request in requests_to_remove:
            lift_people.remove(request)

        #add people waiting if lift passed them when full
        if lift_manager.lift_queue.size() == 0:
            for person in people:
                lift_manager.lift_queue.enqueue(Call(person, False))



        # Get all the people waiting
        people_on_floor = people.count(lift_manager.current_floor)

        if people_on_floor == 0:
            # No one waiting on this floor
            continue

        if people_on_floor > lift_manager.get_free_space():
            # Too many people
            max_can_move = lift_capacity - len(lift_people)
            # Remove people from floor_list
            counter = 0
            for request in people:
                if counter == max_can_move:
                    break
                if request == lift_manager.current_floor:
                    people.remove(request)
                    counter += 1

                    target_floor = random.randint(0, floors - 1)
                    while target_floor == lift_manager.current_floor:
                        target_floor = random.randint(0, floors - 1)

                    lift_manager.lift_queue.enqueue(Call(target_floor, True))
                    lift_people.append(target_floor)
                    lift_manager.add_person()

        else:
            # Can take everyone
            # Removes the people from the list
            people = [request for request in people if request != lift_manager.current_floor]
            for _ in range(people_on_floor):
                # Make a random internal request
                target_floor = random.randint(0, floors - 1)
                while target_floor == lift_manager.current_floor:
                    target_floor = random.randint(0, floors - 1)

                lift_manager.lift_queue.enqueue(Call(target_floor, True))
                lift_people.append(target_floor)
                lift_manager.add_person()

    return total_floors_travelled


"""
TEST 1:
SCAN vs LOOK (Queue)
"""
def scan_vs_look():
    floors_traversed_scan = []
    floors_traversed_look = []
    for algorithm in [Algorithm.SCAN, Algorithm.LOOK]:
        for people in range(DEFAULT_MIN_PEOPLE, DEFAULT_MAX_PEOPLE, DEFAULT_PEOPLE_STEP):
            floors_traversed = random_testing(
                algorithm=algorithm,
                number_of_people=people,
            )

            if algorithm == Algorithm.SCAN:
                floors_traversed_scan.append(floors_traversed)
            elif algorithm == Algorithm.LOOK:
                floors_traversed_look.append(floors_traversed)

    generate_graph(
        floors_traversed_1=floors_traversed_scan,
        people_served=range(DEFAULT_MIN_PEOPLE, DEFAULT_MAX_PEOPLE, DEFAULT_PEOPLE_STEP),
        floors_traversed_2=floors_traversed_look,
        graph_title="SCAN vs LOOK Performance",
        line1_label="SCAN",
        line2_label="LOOK",
    )

    print("Test 1: Ran Successfully")

"""
TEST 2
SCAN vs LOOK (Priority Queue)
"""
def scan_vs_look_prio():
    floors_traversed_scan = []
    floors_traversed_look = []
    for algorithm in [Algorithm.SCAN, Algorithm.LOOK]:
        for people in range(DEFAULT_MIN_PEOPLE, DEFAULT_MAX_PEOPLE, DEFAULT_PEOPLE_STEP):
            floors_traversed = random_testing(
                algorithm=algorithm,
                number_of_people=people,
                use_priority=True
            )

            if algorithm == Algorithm.SCAN:
                floors_traversed_scan.append(floors_traversed)
            elif algorithm == Algorithm.LOOK:
                floors_traversed_look.append(floors_traversed)

    generate_graph(
        floors_traversed_1=floors_traversed_scan,
        people_served=range(DEFAULT_MIN_PEOPLE, DEFAULT_MAX_PEOPLE, DEFAULT_PEOPLE_STEP),
        floors_traversed_2=floors_traversed_look,
        graph_title="SCAN vs LOOK Priority Queue Performance",
        line1_label="SCAN",
        line2_label="LOOK",
    )

    print("Test 2: Ran Successfully")


def scan_vs_look_weight_sensor():
    floors_traversed_scan = []
    floors_traversed_look = []
    floors_traversed_scan_weight = []
    floors_traversed_look_weight = []
    people_served = range(DEFAULT_MIN_PEOPLE, DEFAULT_MAX_PEOPLE, DEFAULT_PEOPLE_STEP)

    for ignore_weight in [True, False]:
        for algorithm in [Algorithm.LOOK, Algorithm.SCAN]:
            for people in people_served:
                floors_traversed = random_testing(
                    algorithm=algorithm,
                    number_of_people=people,
                    ignore_weight=ignore_weight,
                )

                if not ignore_weight:
                    if algorithm == Algorithm.SCAN:
                        floors_traversed_scan_weight.append(floors_traversed)
                    elif algorithm == Algorithm.LOOK:
                        floors_traversed_look_weight.append(floors_traversed)
                else:
                    if algorithm == Algorithm.SCAN:
                        floors_traversed_scan.append(floors_traversed)
                    elif algorithm == Algorithm.LOOK:
                        floors_traversed_look.append(floors_traversed)

    plt.figure(figsize=(8, 6))
    plt.scatter(floors_traversed_scan, people_served, color='blue', label="SCAN - No Sensor", alpha=0.7, marker='o')
    plt.scatter(floors_traversed_scan_weight, people_served, color='darkblue', label="SCAN - Sensor", alpha=0.7, marker='o')
    plt.scatter(floors_traversed_look, people_served, color='red', label="LOOK - No Sensor", alpha=0.7, marker='s')
    plt.scatter(floors_traversed_look_weight, people_served, color='firebrick', label="LOOK - Sensor", alpha=0.7, marker='s')

    plt.xlabel("Floors Traversed")
    plt.ylabel("People Served")
    plt.title("Weight Sensor Performance (SCAN and LOOK)")
    plt.legend()
    plt.grid(True)
    plt.show()

    print("Test 3: Ran Successfully")


"""
TEST 3
Changes in capacity (SCAN vs LOOK)

Settings:
- Use Priority: ON
- Weight Sensor: ON
"""
def capacity_test():
    floors_traversed_scan = []
    floors_traversed_look = []
    graph_y = []
    capacity_list = range(1, 200, 1)
    for _ in range(3): #All tests repeat 3 times
        for algorithm in [Algorithm.SCAN, Algorithm.LOOK]:
            for capacity in capacity_list:
                floors_traversed = random_testing(
                    algorithm=algorithm,
                    lift_capacity=capacity,
                    number_of_people=500
                )

                graph_y.append(capacity)

                if algorithm == Algorithm.SCAN:
                    floors_traversed_scan.append(floors_traversed)
                elif algorithm == Algorithm.LOOK:
                    floors_traversed_look.append(floors_traversed)

    plt.figure(figsize=(8, 6))
    plt.scatter(floors_traversed_scan, graph_y, color='blue', label="SCAN", alpha=0.7, marker='o')
    plt.scatter(floors_traversed_look, graph_y, color='red', label="LOOK", alpha=0.7, marker='s')

    plt.xlabel("Floors Traversed")
    plt.ylabel("Capacity")
    plt.title("How changing lift capacity impacts performance")
    plt.legend()
    plt.grid(True)
    plt.show()


def generate_graph(
        floors_traversed_1 : [int],
        floors_traversed_2 : [int],
        people_served : [int],
        graph_title : str,
        line1_label : str,
        line2_label : str,
):
    plt.figure(figsize=(8, 6))
    plt.scatter(people_served, floors_traversed_1, color='blue', label=line1_label, alpha=0.7, marker='o')
    plt.scatter(people_served, floors_traversed_2, color='red', label=line2_label, alpha=0.7, marker='s')

    plt.xlabel("People Served")
    plt.ylabel("Floors Traversed")
    plt.title(graph_title)
    plt.legend()
    plt.grid(True)
    plt.show()


def run_all_tests():
    scan_vs_look()
    scan_vs_look_prio()
    scan_vs_look_weight_sensor()

if __name__ == '__main__':
    scan_vs_look()