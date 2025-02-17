import random
from turtledemo.penrose import start

from matplotlib import pyplot as plt

from LiftManager import LiftManager
from LiftQueue import LiftQueueR
from LiftQueueCopy import LiftQueue
from Call import Call
from LOOK import look
from SCAN import scan


def file_testing(filename, algorithm, start_floor, start_direction):
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
    lift_queue = LiftQueueR()
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
        #print(f"The lift has traveled from floor {start_floor} to floor {next_floor}. It has traversed {floors_traversed} floor(s).")
        start_direction = new_direction
        start_floor = next_floor

    print()
    print(f"The lift traveled a total of {total_floors_traversed} floor(s) when serving {people_served} people.")
    return floor_requests, people_served


"""
RANDOM_TESTING

ASSUMPTONS:
- Lift has infinite capacity

FUNCTIONS:
- 'People' are just numbers in a list (first the floor they spawn on then the target floor)
- After lift visits every floor once there is no one waiting
"""


def random_testing(algorithm="LOOK", number_of_people=100, lift_capacity=5, ignore_weight=False):
    # print("*" * 40)
    # print(f"TEST USING {algorithm}")
    # print("*" * 40)
    # print()

    # Declares which lift algorithm to use
    lift_algorithm = scan
    if algorithm == "SCAN":
        lift_algorithm = scan


    # Lift Variables
    floors = 5
    people_moved = 0
    current_direction = "up"
    current_floor = 0
    reached_limit = False

    # People lists
    people = []
    lift_people = []

    # Tracking metrics
    total_floors_travelled = 0

    lift_manager = LiftManager(capacity=lift_capacity, direction=current_direction, current_floor=current_floor, floors=floors, ignore_weight=ignore_weight)


    for _ in range(number_of_people):
        starting_floor = random.randint(0, floors)
        lift_manager.lift_queue.enqueue(Call(starting_floor, False))
        people.append(starting_floor)

    while len(people) > 0 or len(lift_people) > 0:
        # Run the loop
        if algorithm == "LOOK":
            lift_data = lift_manager.lift_queue, lift_manager.current_direction, current_floor
            current_direction, next_floor = lift_algorithm(lift_data)
        elif algorithm == "SCAN":
            current_direction, next_floor, reached_limit = lift_manager.scan()

            if reached_limit:
                floors_traversed = 0
                if current_direction == "up":
                    floors_traversed = (floors - lift_manager.current_floor) + (floors - next_floor)
                elif current_direction == "down":
                    floors_traversed = lift_manager.current_floor + next_floor

                total_floors_travelled += floors_traversed

        if not reached_limit:
            total_floors_travelled += abs(next_floor - lift_manager.current_floor)
        lift_manager.current_floor = next_floor

        # Read any calls
        # if lift_manager.lift_queue.isEmpty():
        #     for request in people:
        #         if not lift_manager.lift_queue.contains(request) and not lift_manager.current_floor == request:
        #             lift_manager.lift_queue.enqueue(Call(request, False))
        #
        #     for request in lift_people:
        #         if not lift_manager.lift_queue.contains(request):
        #             lift_manager.lift_queue.enqueue(Call(request, True))


        # Check if anyone needs to get out
        requests_to_remove = []
        for request in lift_people:
            if request == lift_manager.current_floor:
                # this is your floor
                people_moved += 1
                lift_manager.remove_person()
                requests_to_remove.append(request)

        for request in requests_to_remove:
            lift_people.remove(request)


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
                while target_floor == current_floor:
                    target_floor = random.randint(0, floors - 1)

                lift_manager.lift_queue.enqueue(Call(target_floor, True))
                lift_people.append(target_floor)
                lift_manager.add_person()

    print(f"The lift travelled {total_floors_travelled} floors.")
    return total_floors_travelled, people_moved


def floors_vs_people_graph(number_of_tests):
    floors_traversed_scan = []
    people_served_scan = []
    floors_traversed_look = []
    people_served_look = []

    # for algorithm in ["LOOK", "SCAN"]:
    for m in [True, False]:
        for x in range(5, number_of_tests):
            floors_traversed, num_people_served = random_testing("SCAN", number_of_people=x, lift_capacity=20,
                                                                 ignore_weight=m)
            if m:
                floors_traversed_scan.append(floors_traversed)
                people_served_scan.append(num_people_served)
            else:
                floors_traversed_look.append(floors_traversed)
                people_served_look.append(num_people_served)

            # if algorithm == "LOOK":
            #     floors_traversed_look.append(floors_traversed)
            #     people_served_look.append(num_people_served)
            # elif algorithm == "SCAN":
            #     floors_traversed_scan.append(floors_traversed)
            #     people_served_scan.append(num_people_served)

    plt.figure(figsize=(8, 6))
    plt.scatter(floors_traversed_scan, people_served_scan, color='blue', label='Ignore Weight', alpha=0.7, marker='o')
    plt.scatter(floors_traversed_look, people_served_look, color='red', label='Had Weight', alpha=0.7, marker='s')

    plt.xlabel("Floors Traversed")
    plt.ylabel("People Served")
    plt.title("Lift Algorithm Performance: SCAN vs LOOK")
    plt.legend()
    plt.grid(True)
    plt.show()


# for x in range(15):
#     file_testing(f"input{x + 1}.txt", "LOOK", 0, "up")

if __name__ == '__main__':
    floors_vs_people_graph(1000)
    # random_testing("SCAN")