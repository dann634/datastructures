import scan


def run_test(test_name, lift_data):
    print(f"\n=== {test_name} ===")
    result = scan.scan(lift_data)

    floor_requests, internal_requests, direction, floor_to_serve_next, floors_travelled_past = result

    print(f"Floor to serve next: {floor_to_serve_next}")
    print(f"Floors travelled past: {floors_travelled_past}")
    print(f"Current direction: {direction}")
    print("-" * 80)


# TEST 1: Lift starting at 0. External request (UP) at 4
lift_data1 = (
    [[False, False], [False, False], [False, True], [False, False], [True, False], [False, False], [False, False]],  # External request (UP) at 4
    [False] * 7,  # No internal requests
    'up',
    0  # Start at the ground floor
)
run_test("Test 1: Lift starting at 0. External request (UP) at 4", lift_data1)

# TEST 2: Lift starting at 6. External request (DOWN) at 3
lift_data2 = (
    [[False, False], [True, False], [False, False], [False, True], [False, False], [False, False], [True, False]],  # External request (DOWN) at 3
    [False] * 7,  # No internal requests
    'down',
    6  # Start at 6
)
run_test("Test 2: Lift starting at 6. External request (DOWN) at 3", lift_data2)

# TEST 3: Lift starting at the ground floor. External request (DOWN) at 1
lift_data3 = (
    [[False, False], [False, True], [False, False], [False, False], [False, False], [False, False]],  # External request (DOWN) at 2
    [False] * 6,  # No internal requests
    'up',
    0  # Start at the ground floor
)
run_test("Test 3: Lift starting at the ground floor. External request (DOWN) at 1", lift_data3)

# TEST 4: Lift starting at 4. Internal request for 1.
lift_data4 = (
    [[False, False]] * 5,  # No external requests
    [False, True, False, False, False], # Internal request for 1
    'down',
    4 # Start at 4
)
run_test("Test 4: Lift starting at 4. Internal request for 1.", lift_data4)