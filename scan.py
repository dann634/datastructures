def scan(lift_data):
    floor_requests, internal_requests, direction, current_floor = lift_data
    floors_travelled_past = []

    def check_for_up_request(floor_requests, internal_requests, current_floor):
        for floor in range(current_floor, len(floor_requests)):
            if floor_requests[floor][0] or internal_requests[floor]:
                floor_requests[floor][0] = False
                internal_requests[floor] = False
                return floor

    def check_for_down_request(floor_requests, internal_requests, current_floor):
        for floor in range(current_floor, -1, -1):
            if floor_requests[floor][1] or internal_requests[floor]:
                floor_requests[floor][1] = False
                internal_requests[floor] = False
                return floor

    while any(any(row) for row in floor_requests) or any(internal_requests):
        if direction == 'up':
            floor_to_serve_next = check_for_up_request(floor_requests, internal_requests, current_floor)

            if floor_to_serve_next is not None:
                for i in range(current_floor + 1, floor_to_serve_next):
                    floors_travelled_past.append(i)
                lift_data = floor_requests, internal_requests, direction, floor_to_serve_next, floors_travelled_past
                return lift_data

            else:
                for i in range(current_floor + 1, len(floor_requests)):
                    floors_travelled_past.append(i)
                direction = 'down'
                current_floor = len(floor_requests) - 1

        if direction == 'down':
            floor_to_serve_next = check_for_down_request(floor_requests, internal_requests, current_floor)

            if floor_to_serve_next is not None:
                for i in range(current_floor - 1, floor_to_serve_next, -1):
                    floors_travelled_past.append(i)
                lift_data = floor_requests, internal_requests, direction, floor_to_serve_next, floors_travelled_past
                return lift_data

            else:
                for i in range(current_floor - 1, -1, -1):
                    floors_travelled_past.append(i)
                direction = 'up'
                current_floor = 0

    lift_data = floor_requests, internal_requests, direction, None, floors_travelled_past
    return lift_data


def run_test(test_name, lift_data):
    print(f"\n=== {test_name} ===")
    result = scan(lift_data)

    floor_requests, internal_requests, direction, floor_to_serve_next, floors_travelled_past = result

    print(f"Floor to serve next: {floor_to_serve_next}")
    print(f"Floors travelled past: {floors_travelled_past}")
    print(f"Current direction: {direction}")
    print("-" * 30)


# TEST 1: No Requests (Lift should not move)
lift_data1 = (
    [[False, False] for _ in range(5)],  # No floor requests
    [False] * 5,  # No internal requests
    'up',  # Initial direction
    2  # Current floor
)
run_test("Test 1: No Requests", lift_data1)

# TEST 2: Up Requests Only
lift_data2 = (
    [[False, False], [False, False], [False, False], [True, False], [False, False]],
    [False] * 5,  # No internal requests
    'up',
    0  # Start at ground floor
)
run_test("Test 2: Up Requests Only", lift_data2)

# TEST 3: Down Requests Only
lift_data3 = (
    [[False, False], [False, False], [False, True], [False, True], [False, False]],
    [False] * 5,  # No internal requests
    'down',
    0  # Start at top floor
)
run_test("Test 3: Down Requests Only", lift_data3)

# TEST 4: Mixed Up/Down Requests
lift_data4 = (
    [[False, False], [False, False], [False, True], [False, True], [True, False]],
    [False] * 5,  # No internal requests
    'up',
    0  # Start at ground floor
)
run_test("Test 4: Mixed Up/Down Requests", lift_data4)

# TEST 5: Internal Requests
lift_data5 = (
    [[False, False], [False, False], [False, False], [False, False], [False, False]],
    [False, False, True, False, False],  # Internal request at Floor 1
    'up',
    0  # Start at ground floor
)
run_test("Test 5: Internal Requests", lift_data5)

# TEST 6: Mixed External & Internal Requests
lift_data6 = (
    [[False, False], [False, False], [True, False], [False, True], [False, False]],  # External request at Floor 2
    [False, False, False, False, True],  # Internal request at Floor 4
    'up',
    0  # Start at ground floor
)
run_test("Test 6: Internal Requests", lift_data6)