def scan(lift_data):
    # Unpack lift_data tuple
    floor_requests, internal_requests, direction, current_floor = lift_data
    floors_travelled_past = []  # Stores floors passed without stopping

    # Function to check for the next request in the upward direction
    def check_for_up_request(floor_requests, internal_requests, current_floor):
        for floor in range(current_floor, len(floor_requests)):
            if floor_requests[floor][0] or internal_requests[floor]:  # If an up request exists
                floor_requests[floor][0] = False  # Change request to be served
                internal_requests[floor] = False  # Change request to be served
                return floor

    # Function to check for the next request in the downward direction
    def check_for_down_request(floor_requests, internal_requests, current_floor):
        for floor in range(current_floor, -1, -1):
            if floor_requests[floor][1] or internal_requests[floor]:  # If a down request exists
                floor_requests[floor][1] = False  # Change request to be served
                internal_requests[floor] = False  # Change request to be served
                return floor

    # Continue while there are requests either external or internal
    while any(any(row) for row in floor_requests) or any(internal_requests):
        if direction == 'up':
            floor_to_serve_next = check_for_up_request(floor_requests, internal_requests, current_floor)

            if floor_to_serve_next is not None:
                # Record floors travelled past without stopping
                for i in range(current_floor + 1, floor_to_serve_next):
                    floors_travelled_past.append(i)

                # Update lift data and return it
                lift_data = floor_requests, internal_requests, direction, floor_to_serve_next, floors_travelled_past
                return lift_data

            else:
                # If no more requests upwards, travel to the top and change direction
                for i in range(current_floor + 1, len(floor_requests)):
                    floors_travelled_past.append(i)
                direction = 'down'
                current_floor = len(floor_requests) - 1  # Move to the top floor

        if direction == 'down':
            floor_to_serve_next = check_for_down_request(floor_requests, internal_requests, current_floor)

            if floor_to_serve_next is not None:
                # Record floors travelled past without stopping
                for i in range(current_floor - 1, floor_to_serve_next, -1):
                    floors_travelled_past.append(i)

                # Update lift data and return it
                lift_data = floor_requests, internal_requests, direction, floor_to_serve_next, floors_travelled_past
                return lift_data

            else:
                # If no more requests downwards, travel to the ground and change direction
                for i in range(current_floor - 1, -1, -1):
                    floors_travelled_past.append(i)
                direction = 'up'
                current_floor = 0  # Move to the ground floor

    # If no requests remain, return final state
    lift_data = floor_requests, internal_requests, direction, None, floors_travelled_past
    return lift_data