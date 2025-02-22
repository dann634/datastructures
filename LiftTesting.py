import random

from matplotlib import pyplot as plt

from AlgorithmEnum import Algorithm
from LiftManager import LiftManager
from Call import Call

#STANDARD CONSTANTS FOR TESTING
DEFAULT_MIN_PEOPLE = 5
DEFAULT_MAX_PEOPLE = 1000
DEFAULT_PEOPLE_STEP = 5
DEFAULT_LIFT_CAPACITY = 12
DEFAULT_IGNORE_WEIGHT = False
DEFAULT_FLOORS = 30

"""
Runs the tests from the text files
Used to test very specific scenarios
"""
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
    lift_manager = LiftManager.get_instance(
        algorithm=algorithm,
        capacity=lift_capacity,
        direction=start_direction,
        current_floor=start_floor,
        floors=num_floors,
        ignore_weight=DEFAULT_IGNORE_WEIGHT,
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
Randomly selects a floor for a request to spawn on

Args:
    algorithm (Algorithm): the algorithm to use
    test_num (int): the test identifier
    number_of_people (int): the number of people to serve
    lift_capacity (int): how many people the lift can move at once
    ignore_weight (bool): whether to ignore weight
    track_people (bool): whether to track people
    floors (int): the number of floors in the building
    is_last_test (bool): flag to save the example input
    
Returns:
    floors_traversed (int): the aggregate of all floors travelled by the lift
    people_in_lift_track (int): A tracking metric for how many people are in the lift
    floors_travelled_empty (int): A tracking metric for how often the lift is empty
"""
def random_testing(
        algorithm : Algorithm,
        test_num: int,
        number_of_people : int = DEFAULT_MAX_PEOPLE,
        lift_capacity : int = DEFAULT_LIFT_CAPACITY,
        ignore_weight : bool = DEFAULT_IGNORE_WEIGHT,
        track_people : bool = False,
        floors : int = DEFAULT_FLOORS,
        is_last_test : bool = False,
):


    # People lists
    people : [int] = []
    lift_people : [int] = []

    # Create lift instance
    lift_manager = LiftManager.get_instance(
        algorithm=algorithm,
        capacity=lift_capacity,
        direction="up",
        current_floor=0,
        floors=floors,
        ignore_weight=ignore_weight,
    )

    # Populate Floors with People
    for _ in range(number_of_people):
        starting_floor = random.randint(0, floors - 1)
        lift_manager.lift_queue.enqueue(Call(starting_floor, False))
        people.append(starting_floor)

    # Stores extra variables if method passes the boolean flag
    if track_people:
        floors_traversed, people_in_lift_track, floors_travelled_empty, request_log = run_algorithm(lift_manager, people, lift_people, track_people=track_people)
    else:
        floors_traversed, request_log = run_algorithm(lift_manager, people, lift_people)

    #Save input file
    if is_last_test:
        save_random_input(request_log, floors, lift_capacity, test_num)

    # Returns tracking variables if method passes the boolean flag
    if track_people:
        return floors_traversed, people_in_lift_track, floors_travelled_empty
    else:
        return floors_traversed



"""
The main loop for running the lift algorithm
Args:
    lift_manager (LiftManager): LiftManager instances handles the algorithm logic
    people ([int]): List of people represented as integers as the floors they're on
    lift_people ([int]): List of people in the lift represented as integers for the floor they want to go to
    track_people (boolean): Flag for whether the tracking metrics should be returned
    
Returns:
    floors_traversed (int): An aggregate of all the floors travelled by the lift
    request_log (dict): A dictionary containing where internal requests came from
    people_in_lift_track (int): A tracking metric for how many people are in the lift
    floors_travelled_empty (int): A tracking metric for how often the lift is empty
"""
def run_algorithm(lift_manager : LiftManager, people : [int], lift_people : [int], track_people : bool = False):

    # Tracking metrics
    total_floors_travelled = 0
    people_in_lift_track = 0
    floors_travelled_empty = 0

    # Saves test for file storage
    request_log : {int, [int]} = {}

    #Adds empty lists for each floor
    for floor in range(lift_manager.floors):
        request_log[floor] = []

    # Main Lift Loop
    while len(people) > 0 or len(lift_people) > 0:

        # Dequeue Next Request
        next_floor = lift_manager.process_next_request()

        # Used for SCAN (Always False for other algorithms)
        if lift_manager.reached_limit:
            floors_traversed = 0
            if lift_manager.current_direction == "up":
                floors_traversed = (lift_manager.floors - lift_manager.current_floor) + (lift_manager.floors - next_floor)
            elif lift_manager.current_direction == "down":
                floors_traversed = lift_manager.current_floor + next_floor

            # Add floors traversed by the lift to the metric variable
            total_floors_travelled += floors_traversed
            if len(lift_people) == 0:
                floors_travelled_empty += floors_traversed

        # Update tracking metrics
        if not lift_manager.reached_limit:
            total_floors_travelled += abs(next_floor - lift_manager.current_floor)
            if len(lift_people) == 0:
                floors_travelled_empty += abs(next_floor - lift_manager.current_floor)


        # Update lift current position
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

        people_in_lift_track += len(lift_people)

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
            max_can_move = lift_manager.capacity - len(lift_people)
            # Remove people from floor_list
            counter = 0
            for request in people:
                if counter == max_can_move:
                    break
                if request == lift_manager.current_floor:
                    people.remove(request)
                    counter += 1

                    # Create target floor
                    target_floor = random.randint(0, lift_manager.floors - 1)
                    while target_floor == lift_manager.current_floor:
                        target_floor = random.randint(0, lift_manager.floors - 1)

                    lift_manager.lift_queue.enqueue(Call(target_floor, True))
                    lift_people.append(target_floor)
                    lift_manager.add_person()

                    # Add target floor to tracking dictionary
                    request_log[lift_manager.current_floor].append(target_floor)



        else:
            # Can take everyone
            # Removes the people from the list
            people = [request for request in people if request != lift_manager.current_floor]
            for _ in range(people_on_floor):
                # Make a random internal request
                target_floor = random.randint(0, lift_manager.floors - 1)
                while target_floor == lift_manager.current_floor:
                    target_floor = random.randint(0, lift_manager.floors - 1)

                lift_manager.lift_queue.enqueue(Call(target_floor, True), lift_manager.current_floor)
                lift_people.append(target_floor)
                lift_manager.add_person()

                # Add target floor to tracking dictionary
                request_log[lift_manager.current_floor].append(target_floor)


    if track_people:
        return total_floors_travelled, people_in_lift_track, floors_travelled_empty, request_log
    else:
        return total_floors_travelled, request_log


"""
TEST 1:
SCAN vs LOOK vs MyAlgorithm

Testing Values:
People: 1000
Floors: 30
Capacity: 12

Lift Settings:
Weight Sensor: ON
"""
def scan_vs_look_myalgorithm():

    #Lists to store results of each algorithm output
    floors_traversed_scan : [int] = []
    floors_traversed_look : [int] = []
    floors_traversed_myalgorithm : [int] = []

    #Create list from the default values
    people_served = range(DEFAULT_MIN_PEOPLE, DEFAULT_MAX_PEOPLE, DEFAULT_PEOPLE_STEP)

    #Loops through, using each algorithm, changing the number of people each time
    for algorithm in [Algorithm.SCAN, Algorithm.LOOK, Algorithm.MYALGORITHM]:
        for people in people_served:

            #Is last test
            is_last = algorithm == Algorithm.LOOK and people == people_served[-1]

            #Call the random testing method to get floors traversed
            floors_traversed = random_testing(
                algorithm=algorithm,
                number_of_people=people,
                is_last_test=is_last,
                test_num=1
            )

            #Add output to matching list
            match algorithm:
                case Algorithm.SCAN:
                    floors_traversed_scan.append(floors_traversed)
                case Algorithm.LOOK:
                    floors_traversed_look.append(floors_traversed)
                case Algorithm.MYALGORITHM:
                    floors_traversed_myalgorithm.append(floors_traversed)

    #Generate the graph from the data
    generate_graph(
        people_served=people_served,
        graph_title="SCAN vs LOOK vs MyAlgorithm Performance",
        floors_traversed_1=floors_traversed_scan,
        floors_traversed_2=floors_traversed_look,
        floors_traversed_3=floors_traversed_myalgorithm,
        line1_label="SCAN",
        line2_label="LOOK",
        line3_label = "MyAlgorithm",
        test_num=1
    )

    print("Test 1: Ran Successfully")



"""
TEST 2
Testing how a weight sensor affects the efficiency of a lift
(When the lift is full only serve internal calls)

Testing Values:
People: 2000
Capacity: 12
Floors: 30

Lift Settings:
Weight Sensor: (ON/OFF)
"""
def algorithm_weight_sensor_test():

    #Lists to store results of each algorithm output
    floors_traversed_scan : [int] = []
    floors_traversed_look : [int] = []
    floors_traversed_scan_weight : [int] = []
    floors_traversed_look_weight : [int] = []

    # Create list from the default values
    people_served = range(DEFAULT_MIN_PEOPLE, DEFAULT_MAX_PEOPLE, DEFAULT_PEOPLE_STEP)

    # Loops through, using each algorithm, running with the weight sensor on and off, changing the number of people each time
    for ignore_weight in [True, False]:
        for algorithm in [Algorithm.LOOK, Algorithm.SCAN]:
            for people in people_served:

                # Should save file
                is_last = algorithm == Algorithm.LOOK and people == people_served[-1]

                # Get floors traversed from output
                floors_traversed = random_testing(
                    algorithm=algorithm,
                    number_of_people=people,
                    ignore_weight=ignore_weight,
                    test_num=2,
                    is_last_test=is_last
                )


                # Add output to matching list
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


    #Generate graph
    plt.figure(figsize=(8, 6))
    plt.scatter(people_served, floors_traversed_scan, color='blue', label="SCAN - No Sensor", alpha=0.7, marker='o')
    plt.scatter(people_served, floors_traversed_scan_weight, color='darkblue', label="SCAN - Sensor", alpha=0.7, marker='o')
    plt.scatter(people_served, floors_traversed_look, color='red', label="LOOK - No Sensor", alpha=0.7, marker='s')
    plt.scatter(people_served, floors_traversed_look_weight, color='firebrick', label="LOOK - Sensor", alpha=0.7, marker='s')

    #Add details to the graph
    plt.xlabel("People Served")
    plt.ylabel("Floors Traversed")
    plt.title("Weight Sensor Performance (SCAN, LOOK, MyAlgorithm)")
    plt.legend()
    plt.grid(True)
    plt.savefig("tests/test2/graph.png")
    plt.show()

    print("Test 2: Ran Successfully")


"""
TEST 3
Changes in capacity (SCAN vs LOOK)

Testing Values:
People: 2000
Capacity - (1-500)
Floors: 30

Settings:
- Use Priority: ON
- Weight Sensor: ON
"""
def capacity_test():

    # Lists to store output of algorithms
    floors_traversed_scan : [int] = []
    floors_traversed_look : [int] = []
    floors_traversed_myalgorithm : [int] = []
    graph_y : [int] = []

    #The list of capacity values the test uses
    capacity_list = range(1, 500, 1)

    for algorithm in [Algorithm.SCAN, Algorithm.LOOK, Algorithm.MYALGORITHM]:
        for capacity in capacity_list:

            # Is last test
            is_last = algorithm == Algorithm.LOOK and capacity == capacity_list[-1]

            floors_traversed = random_testing(
                algorithm=algorithm,
                lift_capacity=capacity,
                number_of_people=500,
                test_num=3,
                is_last_test=is_last
            )


            # Add output to matching list
            if algorithm == Algorithm.SCAN:
                floors_traversed_scan.append(floors_traversed)
                graph_y.append(capacity)
            elif algorithm == Algorithm.LOOK:
                floors_traversed_look.append(floors_traversed)
            elif algorithm == Algorithm.MYALGORITHM:
                floors_traversed_myalgorithm.append(floors_traversed)


    # Create graphs for individual algorithms
    generate_single_graph(floors_traversed_look, graph_y, "LOOK", "red", "How changing lift capacity impacts performance", apply_x_limit=True, test_num=4, subtitle="LOOK")
    generate_single_graph(floors_traversed_scan, graph_y, "SCAN", "blue", "How changing lift capacity impacts performance", apply_x_limit=True, test_num=4, subtitle="SCAN")
    generate_single_graph(floors_traversed_myalgorithm, graph_y, "MyAlgorithm", "darkblue", "How changing lift capacity impacts performance", apply_x_limit=True, test_num=4, subtitle="MyAlgorithm")


    #Add all the data to one graph
    plt.figure(figsize=(8, 6))
    plt.scatter(floors_traversed_scan, graph_y, color='blue', label="SCAN", alpha=0.7, marker='o')
    plt.scatter(floors_traversed_look, graph_y, color='red', label="LOOK", alpha=0.7, marker='s')
    plt.scatter(floors_traversed_myalgorithm, graph_y, color='darkblue', label="MyAlgorithm", alpha=0.7, marker='s')

    plt.xlim(0, 4000)
    plt.xlabel("Floors Traversed")
    plt.ylabel("Capacity")
    plt.title("How changing lift capacity impacts performance")
    plt.legend()
    plt.grid(True)
    plt.savefig("tests/test3/graph.png")
    plt.show()

    print("Test 3: Ran Successfully")


"""
TEST 4
All requests coming from a few floors (SCAN vs LOOK)

Testing Values:
People: 1000
Floors: 30
Capacity: 12

Lift Settings:
- Weight Sensor: ON
"""
def popular_floor_test(random_floors : int = 3):

    # Variables for floors
    floors = DEFAULT_FLOORS
    number_of_random_floors = random_floors

    # Lists to store output of algorithms
    floors_traversed_scan : [int] = []
    floors_traversed_look : [int] = []
    floors_traversed_myalgorithm : [int] = []

    # List of values for people
    people_served = range(DEFAULT_MIN_PEOPLE, DEFAULT_MAX_PEOPLE, 2)

    # Loop through each algorithm
    for algorithm in [Algorithm.SCAN, Algorithm.LOOK, Algorithm.MYALGORITHM]:
        for people in people_served:
            random_floors = []

            # Choose random floors
            while len(random_floors) < number_of_random_floors:
                # Choose a random floor to overload
                chosen_floor = random.randint(0, floors - 1)
                while chosen_floor in random_floors:
                    chosen_floor = random.randint(0, floors - 1)
                random_floors.append(chosen_floor)

            # Add people randomly to the chosen floors
            people_list = []
            for _ in range(people):
                people_list.append(random.choice(random_floors))

            lift_people: [int] = []

            # Setup lift with all the values
            lift_manager = LiftManager.get_instance(
                algorithm=algorithm,
                capacity=DEFAULT_LIFT_CAPACITY,
                direction="up",
                current_floor=0,
                floors=floors,
                ignore_weight=DEFAULT_IGNORE_WEIGHT,
            )

            # Get output of algorithm
            floors_travelled, request_log = run_algorithm(lift_manager, people_list, lift_people)

            # Save last look input file
            if algorithm == Algorithm.LOOK and people == people_served[-1]:
                save_random_input(request_log, floors, DEFAULT_LIFT_CAPACITY, test_num=4)

            # Store output to matching list
            if algorithm == Algorithm.SCAN:
                floors_traversed_scan.append(floors_travelled)
            elif algorithm == Algorithm.LOOK:
                floors_traversed_look.append(floors_travelled)
            elif algorithm == Algorithm.MYALGORITHM:
                floors_traversed_myalgorithm.append(floors_travelled)

    # Create graph from data
    generate_graph(
        people_served=people_served,
        graph_title="SCAN vs Look vs MyAlgorithm when 3 floors have lots of requests",
        floors_traversed_1=floors_traversed_scan,
        floors_traversed_2=floors_traversed_look,
        floors_traversed_3=floors_traversed_myalgorithm,
        line1_label="SCAN",
        line2_label="LOOK",
        line3_label="MyAlgorithm",
        test_num=4
    )

    print("Test 4: Ran Successfully")



"""
Average Occupancy of Lift over Floors Travelled

Testing Values:
People: 1000
Floors: 30
Capacity: 12

Lift Settings:
- Weight Sensor: ON
"""
def lift_occupancy_test():
    # Lists to store results of each algorithm output
    average_people_scan : [float] = []
    average_people_look : [float] = []
    average_people_myalgorithm : [float] = []

    # Create list from the default values
    people_served = range(DEFAULT_MIN_PEOPLE, DEFAULT_MAX_PEOPLE, 1)

    # Loops through, using each algorithm, changing the number of people each time
    for algorithm in [Algorithm.SCAN, Algorithm.LOOK, Algorithm.MYALGORITHM]:
        for people in people_served:

            # Is last request (save to file)
            is_last = algorithm == Algorithm.LOOK and people == people_served[-1]

            # Call the random testing method to get floors traversed
            floors_traversed, people_in_lift, _ = random_testing(
                algorithm=algorithm,
                number_of_people=people,
                track_people=True,
                test_num=5,
                is_last_test=is_last,
            )

            # Calculate average
            average = 0
            if not floors_traversed == 0:
                average = people_in_lift / floors_traversed

            # Add output to matching list
            match algorithm:
                case Algorithm.SCAN:
                    average_people_scan.append(average)
                case Algorithm.LOOK:
                    average_people_look.append(average)
                case Algorithm.MYALGORITHM:
                    average_people_myalgorithm.append(average)

    # Generate the graph from the data
    generate_graph(
        people_served=people_served,
        graph_title="Comparison of the average occupancy",
        floors_traversed_1=average_people_scan,
        floors_traversed_2=average_people_look,
        floors_traversed_3=average_people_myalgorithm,
        line1_label="SCAN",
        line2_label="LOOK",
        line3_label="MyAlgorithm",
        y_label = "Average People in Lift",
        apply_y_limit=True,
        test_num=5
    )

    print("Test 5: Ran Successfully")



"""
Testing how often the lift is travelling empty

Testing Values:
People: 1000
Floors: 30
Capacity: 12

Lift Settings:
- Weight Sensor: ON
"""
def floor_test():
    # Lists to store results of each algorithm output
    percent_time_scan : [float ]= []
    percent_time_look : [float] = []
    percent_time_myalgorithm : [float] = []
    # Create list from the default values
    people_served = range(DEFAULT_MIN_PEOPLE, DEFAULT_MAX_PEOPLE, 2)

    # Loops through, using each algorithm, changing the number of people each time
    for algorithm in [Algorithm.SCAN, Algorithm.LOOK, Algorithm.MYALGORITHM]:
        for people in people_served:

            # Is last request (save input to file)
            is_last = algorithm == Algorithm.LOOK and people == people_served[-1]

            # Call the random testing method to get floors traversed
            floors_traversed, _, floors_travelled_empty = random_testing(
                algorithm=algorithm,
                number_of_people=people,
                track_people=True,
                test_num=6,
                is_last_test=is_last,
            )

            percent_time = floors_travelled_empty / floors_traversed

            # Add output to matching list
            match algorithm:
                case Algorithm.SCAN:
                    percent_time_scan.append(percent_time)
                case Algorithm.LOOK:
                    percent_time_look.append(percent_time)
                case Algorithm.MYALGORITHM:
                    percent_time_myalgorithm.append(percent_time)

    generate_single_graph(people_served, percent_time_scan, "SCAN", "blue", "Floors travelled while not carrying anyone", y_label="Percent Time Lift is Empty", test_num=6, subtitle="SCAN")
    generate_single_graph(people_served, percent_time_look, "LOOK", "red","Floors travelled while not carrying anyone", y_label="Percent Time Lift is Empty", test_num=6, subtitle="LOOK")
    generate_single_graph(people_served, percent_time_myalgorithm, "MyAlgorithm", "darkblue","Floors travelled while not carrying anyone", y_label="Percent Time Lift is Empty", test_num=6, subtitle="MyAlgorithm")

    # Generate the graph from the data
    generate_graph(
        people_served=people_served,
        graph_title="Floors travelled while not carrying anyone",
        floors_traversed_1=percent_time_scan,
        floors_traversed_2=percent_time_look,
        floors_traversed_3=percent_time_myalgorithm,
        line1_label="SCAN",
        line2_label="LOOK",
        line3_label="MyAlgorithm",
        y_label = "Percent Time Lift is Empty",
        test_num=6
    )

    print("Test 6: Ran Successfully")


"""
Generates the graphs from the data provided
Plots floors traversed against the amount of people being served
Saves the graph to a png file

Args:
    people_served ([int]): the values for the x axis
    graph_title (str): the title for the graph
    floors_traversed_1 ([int]): the values for the y axis
    floors_traversed_2 ([int]): the values for the y axis
    floors_traversed_3 ([int]): the values for the y axis
    line1_label (str): the label for the floors_traversed_1 values
    line2_label (str): the label for the floors_traversed_2 values
    line3_label (str): the label for the floors_traversed_3 values
    test_num (int): the test identifier
    x_label (str): the label for the x axis
    y_label (str): the label for the y axis
    apply_y_limit (bool): whether to limit the y axis or not
"""
def generate_graph(
        people_served: [int],
        graph_title: str,
        floors_traversed_1 : [int],
        floors_traversed_2 : [int],
        floors_traversed_3 : [int],
        line1_label : str,
        line2_label : str,
        line3_label : str,
        test_num : int,
        x_label : str = "People Served",
        y_label : str = "Floors Traversed",
        apply_y_limit: bool = False,

):
    plt.figure(figsize=(8, 6))
    plt.scatter(people_served, floors_traversed_1, color='blue', label=line1_label, alpha=0.7, marker='o')
    plt.scatter(people_served, floors_traversed_2, color='red', label=line2_label, alpha=0.7, marker='o')
    plt.scatter(people_served, floors_traversed_3, color='darkblue', label=line3_label, alpha=0.7, marker='o')

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    if apply_y_limit:
        plt.ylim(0, 12)
    plt.title(graph_title)
    plt.legend()
    plt.grid(True)
    plt.savefig(f"tests/test{test_num}/graph.png")
    plt.show()

"""
Generates a graph for only one algorithm
(Used when the data is overlapping or messy)
Saves the graph to a png file

Args:
    x_values ([int]): the list of values for the x axis
    y_values ([int]): the list of values for the y axis
    label (str): the label for the line
    title (str): the title for the graph
    test_num (int): the test identifier
    subtitle (str): the subtitle for the graph save file
    x_label (str): the label for the x axis
    y_label (str): the label for the y axis
    apply_x_limit (bool): whether to limit the x axis or not
"""
def generate_single_graph(x_values : [int],
                          y_values : [int],
                          label : str,
                          color: str,
                          title: str,
                          test_num: int,
                          subtitle : str,
                          x_label : str = "People Served",
                          y_label : str = "Floors Traversed",
                          apply_x_limit : bool = False,
                          ):

    # Print out each graph separately first
    plt.figure(figsize=(8, 6))
    plt.scatter(x_values, y_values, color=color, label=label, alpha=0.7, marker='o')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    if apply_x_limit:
        plt.xlim(0, 4000)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.savefig(f"tests/test{test_num}/graph_{subtitle}.png")
    plt.show()


"""
Saves input for tests in a text file using the standard format

Args:
    request_log (dict): A dictionary which holds which floor the internal requests came from
    floors (int): the number of floors in the building
    capacity (int): how many people can fit in the lift at once
    test_num (int): the test identifier
"""
def save_random_input(
    request_log,
    floors : int,
    capacity : int,
    test_num : int
):
    file_contents : [str] = []

    # Add headers
    file_contents.append("# Number of Floors, Capacity")
    file_contents.append(f"{floors}, {capacity}")
    file_contents.append("")
    file_contents.append("# Floor Requests")

    # Add requests
    for floor in range(floors):
        internal_requests = request_log[floor]
        request_line = f"{floor}: "
        for request in internal_requests:
            request_line += f"{request}, "
        file_contents.append(request_line)

    #Save to file
    with open(f"tests/test{test_num}/example_input.txt", "w") as f:
        for line in file_contents:
            f.write(f"{line}\n")




"""
Executes all tests sequentially
Saves an example input file and graph to tests/
"""
def run_all_tests():
    scan_vs_look_myalgorithm()
    algorithm_weight_sensor_test()
    capacity_test()
    popular_floor_test()
    lift_occupancy_test()
    floor_test()

if __name__ == '__main__':
    run_all_tests()
