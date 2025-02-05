from LiftQueue import LiftQueue


def look(lift_data):
    lift_queue, current_direction, current_floor = lift_data
    next_floor = LiftQueue.dequeue(lift_queue).requested_floor

    at_target_floor = False
    while not at_target_floor:
        if next_floor == current_floor or next_floor is None:
            at_target_floor = True
        elif next_floor > current_floor and current_direction == "up":
            at_target_floor = True
        elif next_floor < current_floor and current_direction == "down":
            at_target_floor = True
        else:
            current_direction = "down" if current_direction == "up" else "up"
    return current_direction, next_floor