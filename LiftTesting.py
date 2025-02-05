import random
import LiftQueue
import Call
import SCAN
import LOOK


def populate_lift_queue(lift_queue : LiftQueue, num_calls: int, max_floor: int):
    for _ in range(num_calls):
        requested_floor = random.randint(1, max_floor)
        is_internal = random.choice([True, False])
        lift_queue.enqueue(Call.Call(requested_floor, is_internal))
    return lift_queue


def lift_tests(num_tests, max_floor, algorithm):
    lift_queue = populate_lift_queue(LiftQueue.LiftQueue(), num_tests, max_floor)
    current_direction = random.choice(["up", "down"])
    current_floor = random.randint(1, max_floor)
    print("*" * 30)
    print(f"TESTS USING {algorithm} ALGORITHM")
    print("*" * 30)
    print()

    for x in range(num_tests):
        print(f"TEST {x + 1}:")
        print(f"Current Floor: {current_floor}")
        print(f"Current Direction: {current_direction}")
        print(f"Next Floor Request: {lift_queue.peek().requested_floor}")
        print()

        if algorithm == "SCAN":
            lift_data = 0, max_floor, lift_queue, current_direction, current_floor
            current_direction, next_floor, reached_limit = SCAN.scan(lift_data)
        elif algorithm == "LOOK":
            lift_data = lift_queue, current_direction, current_floor
            current_direction, next_floor = LOOK.look(lift_data)

        print(f"Next Floor Served: {next_floor}")
        print(f"Current Direction: {current_direction}")

        if algorithm == "SCAN":
            print(f"Reached Limit: {reached_limit}")
        print("-" * 30)

        current_floor = next_floor

lift_tests(5, 10, "LOOK")






