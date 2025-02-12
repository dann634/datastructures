import random
from turtledemo.penrose import start

from matplotlib import pyplot as plt

from LiftQueue import LiftQueue
from Call import Call
from LOOK import look
from SCAN import scan


def file_testing(filename, algorithm, start_floor, start_direction, min_floor=0):
    print("*" * 40)
    print(f"TEST USING {algorithm} WITH FILE {filename}")
    print("*" * 40)
    print()

    with open(filename, "r") as file:
        file_lines = file.readlines()
        file.close()

    num_floors, min_floor, lift_capacity = file_lines[1].split(",")
    num_floors = int(num_floors.strip())
    min_floor = int(min_floor.strip())
    max_floor = min_floor + num_floors
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
    lift_queue = LiftQueue()
    while floor_requests:
        people_served = people_served + 1
        external_floor_request = random.choice(list(floor_requests.keys()))
        lift_queue.enqueue(Call(external_floor_request, False))

        internal_floor_request = floor_requests[external_floor_request][0]
        lift_queue.enqueue(Call(internal_floor_request, True))

        floor_requests[external_floor_request].pop(0)

        if len(floor_requests[external_floor_request]) < 1:
            del floor_requests[external_floor_request]

    floors_traversed = 0
    total_floors_traversed = 0

    for x in range(lift_queue.size()):
        if algorithm == "LOOK":
            lift_data = lift_queue, start_direction, start_floor
            new_direction, next_floor = look(lift_data)
            floors_traversed = abs(start_floor - next_floor)

        elif algorithm == "SCAN":
            lift_data = min_floor, max_floor, lift_queue, start_direction, start_floor
            new_direction, next_floor, reached_limit = scan(lift_data)

            if reached_limit:
                if start_direction == "up":
                    floors_traversed = (max_floor - start_floor) + (max_floor - next_floor)
                elif start_direction == "down":
                    floors_traversed = (start_floor - min_floor) + (next_floor - min_floor)

            else:
                floors_traversed = abs(start_floor - next_floor)

        total_floors_traversed = total_floors_traversed + floors_traversed
        print(
            f"The lift has traveled from floor {start_floor} to floor {next_floor}. It has traversed {floors_traversed} floor(s). ")
        start_direction = new_direction
        start_floor = next_floor

    print()
    print(f"The lift traveled a total of {total_floors_traversed} floor(s) when serving {people_served} people.")


"""
RANDOM_TESTING

ASSUMPTONS:
- Lift has infinite capacity

FUNCTIONS:
- 'People' are just numbers in a list (first the floor they spawn on then the target floor)
- After lift visits every floor once there is no one waiting
"""


def random_testing(algorithm="LOOK"):
    print("*" * 40)
    print(f"TEST USING {algorithm}")
    print("*" * 40)
    print()

    # Declares which lift algorithm to use
    lift_algorithm = look
    if algorithm == "SCAN":
        lift_algorithm = scan

    lift_queue = LiftQueue()

    # Lift Variables
    floors = 5
    number_of_people = 50
    people_moved = 0
    current_direction = "up"
    current_floor = 0

    lift_capacity = 10

    # People lists
    people = []
    lift_people = []

    # Tracking metrics
    total_floors_travelled = 0

    for _ in range(number_of_people):
        starting_floor = random.randint(0, floors)
        lift_queue.enqueue(Call(starting_floor, False))
        people.append(starting_floor)

    while len(people) > 0 or len(lift_people) > 0:
        # Run the loop
        lift_data = lift_queue, current_direction, current_floor
        current_direction, next_floor = lift_algorithm(lift_data)
        total_floors_travelled += abs(next_floor - current_floor)
        current_floor = next_floor

        # Read any calls
        for request in people:
            if not lift_queue.contains(request):
                lift_queue.enqueue(Call(request, False))

        for request in lift_people:
            if not lift_queue.contains(request):
                lift_queue.enqueue(Call(request, True))

        # Check if anyone needs to get out
        for request in lift_people:
            if request == current_floor:
                # this is your floor
                people_moved += 1
                print(f"Person successfully moved to {request}. {people_moved} people moved.")
                lift_people.remove(request)

        # Get all the people waiting
        people_on_floor = people.count(current_floor)

        if len(lift_people) + people_on_floor > lift_capacity:
            # Too many people
            max_can_move = lift_capacity - len(lift_people)
            # Remove people from floor_list
            counter = 0
            for request in people:
                if counter == max_can_move:
                    break
                if request == current_floor:
                    people.remove(request)
                    counter += 1

        else:
            # Can take everyone
            # Removes the people from the list
            people = [request for request in people if request != current_floor]
            for _ in range(people_on_floor):
                # Make a random internal request
                target_floor = random.randint(0, floors)
                while target_floor == current_floor:
                    target_floor = random.randint(0, floors)

                lift_queue.enqueue(Call(target_floor, True))
                lift_people.append(target_floor)

    print(f"The lift travelled {total_floors_travelled} floors.")


def floors_vs_people_graph(number_of_tests, testing_type="random"):
    floors_traversed_scan = []
    people_served_scan = []
    floors_traversed_look = []
    people_served_look = []

    for x in range(number_of_tests):
        algorithm = random.choice(["LOOK", "SCAN"])

        if testing_type == "random":
            floors_traversed, num_people_served = random_testing(algorithm)
        elif testing_type == "file":
            random_number = random.randint(1, 15)
            input_file = f"input{random_number}.txt"
            floors_traversed, num_people_served = file_testing(input_file, algorithm, 0, "up")

        if algorithm == "LOOK":
            floors_traversed_look.append(floors_traversed)
            people_served_look.append(num_people_served)
        elif algorithm == "SCAN":
            floors_traversed_scan.append(floors_traversed)
            people_served_scan.append(num_people_served)

    plt.figure(figsize=(8, 6))
    plt.scatter(floors_traversed_scan, people_served_scan, color='blue', label='SCAN', alpha=0.7, marker='o')
    plt.scatter(floors_traversed_look, people_served_look, color='red', label='LOOK', alpha=0.7, marker='s')

    plt.xlabel("Floors Traversed")
    plt.ylabel("People Served")
    plt.title("Lift Algorithm Performance: SCAN vs LOOK")
    plt.legend()
    plt.grid(True)
    plt.show()
