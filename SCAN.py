from LiftQueue import LiftQueue


def scan(lift_data):

    reached_limit = False
    min_floor, max_floor, lift_queue, current_direction, current_floor = lift_data
    next_floor = lift_queue.dequeue().requested_floor

    at_target_floor = False
    while not at_target_floor:
        if next_floor == current_floor or next_floor is None:
            at_target_floor = True
        elif next_floor > current_floor and current_direction == "up":
            at_target_floor = True
        elif next_floor < current_floor and current_direction == "down":
            at_target_floor = True
        else:
            if current_direction == "up":
                current_floor = max_floor
                current_direction = "down"
            elif current_direction == "down":
                current_floor = min_floor
                current_direction = "up"
            reached_limit = True
    return current_direction, next_floor, reached_limit