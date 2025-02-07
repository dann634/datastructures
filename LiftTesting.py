import random
import LiftQueue
import Call
from LOOK import look


def lift_test(filename, algorithm):
    print("*" * 40)
    print(f"TEST USING {algorithm} WITH FILE {filename}")
    print("*" * 40)
    print()

    with open(filename, "r") as file:
        file_lines = file.readlines()
        file.close()

    num_floors, lift_capacity = file_lines[1].split(",")
    num_floors = int(num_floors.strip())
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

    current_direction = "up"
    current_floor = 0
    print(f"The lift starts on floor {current_floor} and is travelling {current_direction}.")

    lift_queue = LiftQueue.LiftQueue()
    while floor_requests:
        external_floor_request = random.choice(list(floor_requests.keys()))
        print(f"There is an external lift request at floor {external_floor_request}.")
        lift_queue.enqueue(Call.Call(external_floor_request, False))
        lift_data = lift_queue, current_direction, current_floor
        current_direction, next_floor = look(lift_data)
        current_floor = next_floor
        print(f"The lift is now on floor {current_floor} and is travelling {current_direction}.")

        internal_floor_request = floor_requests[external_floor_request][0]
        print(f"A person has entered the lift and has made an internal request for floor {external_floor_request}.")
        lift_data = lift_queue, current_direction, current_floor
        lift_queue.enqueue(Call.Call(internal_floor_request, True))
        current_direction, next_floor = look(lift_data)
        current_floor = next_floor
        print(f"The lift is now on floor {current_floor} and is travelling {current_direction}.")

        floor_requests[external_floor_request].pop(0)

        if len(floor_requests[external_floor_request]) < 1:
            del floor_requests[external_floor_request]


lift_test("input1.txt", "SCAN")
