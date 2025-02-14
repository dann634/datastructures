from LiftQueueCopy import LiftQueue


class LiftManager:
    def __init__(self, capacity, direction, current_floor):
        self.capacity = capacity
        self.passenger_count = 0
        self.lift_queue = LiftQueue()
        self.current_direction = direction
        self.current_floor = current_floor
