import random
from LiftQueueCopy import LiftQueue
from Call import Call
from LOOK import look
from SCAN import scan


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


    lift_queue = LiftQueue()



    current_direction = "up"
    current_floor = 0
    print(f"The lift starts on floor {current_floor} and is travelling {current_direction}.")

    while floor_requests:
        external_floor_request = random.choice(list(floor_requests.keys()))
        print(f"There is an external lift request at floor {external_floor_request}.")
        lift_queue.enqueue(Call(external_floor_request, False))
        lift_data = lift_queue, current_direction, current_floor
        current_direction, next_floor = look(lift_data)
        current_floor = next_floor
        print(f"The lift is now on floor {current_floor} and is travelling {current_direction}.")

        internal_floor_request = floor_requests[external_floor_request][0]
        print(f"A person has entered the lift and has made an internal request for floor {external_floor_request}.")
        lift_data = lift_queue, current_direction, current_floor
        lift_queue.enqueue(Call(internal_floor_request, True))
        current_direction, next_floor = look(lift_data)
        current_floor = next_floor
        print(f"The lift is now on floor {current_floor} and is travelling {current_direction}.")

        floor_requests[external_floor_request].pop(0)

        if len(floor_requests[external_floor_request]) < 1:
            del floor_requests[external_floor_request]


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

    #Declares which lift algorithm to use
    lift_algorithm = look
    if algorithm == "SCAN":
        lift_algorithm = scan

    lift_queue = LiftQueue()

    #Lift Variables
    floors = 5
    number_of_people = 5000
    people_moved = 0
    current_direction = "up"
    current_floor = 0

    lift_capacity = 1

    #People lists
    people = []
    lift_people = []

    #Tracking metrics
    total_floors_travelled = 0

    for _ in range(number_of_people):
        starting_floor = random.randint(0, floors)
        lift_queue.enqueue(Call(starting_floor, False))
        people.append(starting_floor)

    while len(people) > 0 or len(lift_people) > 0:
        #Run the loop
        lift_data = lift_queue, current_direction, current_floor
        current_direction, next_floor = lift_algorithm(lift_data)
        total_floors_travelled += abs(next_floor - current_floor)
        current_floor = next_floor

        #Read any calls
        if lift_queue.isEmpty():
            for request in people:
                if not lift_queue.contains(request) and not current_floor == request:
                    lift_queue.enqueue(Call(request, False))

            for request in lift_people:
                if not lift_queue.contains(request):
                    lift_queue.enqueue(Call(request, True))


        #Check if anyone needs to get out
        requests_to_remove = []
        for request in lift_people:
            if request == current_floor:
                #this is your floor
                people_moved += 1
                print(f"Person successfully moved to {request}. {people_moved} people moved.")
                requests_to_remove.append(request)

        for request in requests_to_remove:
            lift_people.remove(request)


        #Get all the people waiting
        people_on_floor = people.count(current_floor)

        if people_on_floor == 0:
            #No one waiting on this floor
            continue

        if len(lift_people) + people_on_floor > lift_capacity:
            #Too many people
            max_can_move = lift_capacity - len(lift_people)
            #Remove people from floor_list
            counter = 0
            for request in people:
                if counter == max_can_move: #Maybe start counter at 1
                    break
                if request == current_floor:
                    people.remove(request)
                    counter += 1

                    target_floor = random.randint(0, floors - 1)
                    while target_floor == current_floor:
                        target_floor = random.randint(0, floors - 1)

                    lift_queue.enqueue(Call(target_floor, True))
                    lift_people.append(target_floor)

        else:
            #Can take everyone
            # Removes the people from the list
            people = [request for request in people if request != current_floor]
            for _ in range(people_on_floor):
                # Make a random internal request
                target_floor = random.randint(0, floors - 1)
                while target_floor == current_floor:
                    target_floor = random.randint(0, floors - 1)

                lift_queue.enqueue(Call(target_floor, True))
                lift_people.append(target_floor)


    print(f"The lift travelled {total_floors_travelled} floors.")










random_testing("LOOK")
# lift_test("input1.txt", "SCAN")
