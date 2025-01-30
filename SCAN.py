def scan(requests, current_direction, current_floor):

    def check_for_next_request(requests, current_direction, current_floor):
        next_floor = PRIORITY_QUEUE.DEQUEUE(current_direction, current_floor)
        return next_floor

    if current_direction == 'up':



