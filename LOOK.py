def look(lift_data):
    lift_queue, current_direction, current_floor = lift_data
    next_floor = lift_queue.dequeue().requested_floor  # Gets the next floor from the queue

    # If the lift is already at the requested floor or no request exists
    if next_floor is None:
        return current_direction, current_floor

    # If the lift is moving up and the requested floor is above the current floor
    elif next_floor > current_floor and current_direction == "up":
        return current_direction, next_floor

    # If the lift is moving down and the requested floor is below the current floor
    elif next_floor < current_floor and current_direction == "down":
        return current_direction, next_floor

    # If the lift is moving in the wrong direction the direction is flipped
    elif current_direction == "up":
        return "down", next_floor
    elif current_direction == "down":
        return "up", next_floor
