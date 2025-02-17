def scan(lift_data):

    reached_limit = False # Boolean to determine whether the lift has gone to the top or bottom of the building
    min_floor, max_floor, lift_queue, current_direction, current_floor = lift_data
    next_floor = lift_queue.dequeue().requested_floor # Gets the next floor from the queue

    at_target_floor = False # Boolean to determine whether the lift has arrived at the next destination.
    while not at_target_floor:

        # If the lift is already at the requested floor or no request exists
        if next_floor == current_floor or next_floor is None:
            at_target_floor = True

        # If the lift is moving up and the requested floor is above the current floor
        elif next_floor > current_floor and current_direction == "up":
            at_target_floor = True

        # If the lift is moving down and the requested floor is below the current floor
        elif next_floor < current_floor and current_direction == "down":
            at_target_floor = True

        # If the lift cannot continue in the same direction, it reverses at the top or bottom of the building
        else:
            if current_direction == "up":
                current_floor = max_floor # Lift moves to the highest floor
                current_direction = "down" # Direction is changed to downwards

            elif current_direction == "down":
                current_floor = min_floor # Lift moves to the lowest floor
                current_direction = "up" # Direction is changed to upwards

            reached_limit = True # Made true to show that the lift has gone to the top or bottom of the building

    return current_direction, next_floor, reached_limit