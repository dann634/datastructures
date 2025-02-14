def look(lift_data):
    lift_queue, current_direction, current_floor, num_people_in_lift, capacity = lift_data
    next_request = lift_queue.dequeue()
    next_floor = next_request.requested_floor  # Gets the next floor from the queue
    is_internal = next_request.is_internal

    # If the lift is already at the requested floor or no request exists
    if next_floor is None:
        return current_direction, current_floor

    # If the lift is moving up and the requested floor is above the current floor
    if next_floor > current_floor and current_direction == "up":




        num_people_in_lift += -1 if is_internal else 1
        return current_direction, next_floor

        # If the lift is moving down and the requested floor is below the current floor
    elif next_floor < current_floor and current_direction == "down":
        num_people_in_lift += -1 if is_internal else 1
        return current_direction, next_floor

        # If the lift is moving in the wrong direction the direction is flipped
    elif current_direction == "up":
        num_people_in_lift += -1 if is_internal else 1
        return "down", next_floor
    elif current_direction == "down":
        num_people_in_lift += -1 if is_internal else 1
        return "up", next_floor
