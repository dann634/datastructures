from LiftQueueCopy import LiftQueue
from AlgorithmEnum import Algorithm


class LiftManager:
    def __init__(self, algorithm, capacity, direction, current_floor, floors, ignore_weight):
        self.capacity = capacity
        self.passenger_count = 0
        self.lift_queue = LiftQueue()
        self.current_direction = direction
        self.current_floor = current_floor
        self.floors = floors
        self.ignore_weight = ignore_weight
        self.algorithm = algorithm

        # SCAN ONLY
        self.reached_limit = False

    def process_next_request(self):
        match self.algorithm:
            case Algorithm.LOOK:
                return self.__look()
            case Algorithm.SCAN:
                return self.__scan()

    def __scan(self):
        self.reached_limit = False  # Boolean to determine whether the lift has gone to the top or bottom of the building

        next_request = self.lift_queue.dequeue(self.ignore_weight,self.is_lift_full()).requested_floor  # Gets the next request from the queue

        if next_request is None:
            return self.current_direction, self.current_floor, self.reached_limit

        next_floor = next_request.requested_floor

        # If the lift is already at the requested floor or no request exists
        if next_floor == self.current_floor:
            return self.current_direction, next_floor, self.reached_limit

        # Move in the correct direction
        if self.current_direction == "up":
            if next_floor > self.current_floor:
                self.current_floor = next_floor  # Move to the next floor
            else:
                self.current_direction = "down"
                self.reached_limit = True
                self.current_floor = next_floor  # Move to the next floor

        elif self.current_direction == "down":
            if next_floor < self.current_floor:
                self.current_floor = next_floor  # Move to the next floor
            else:
                self.current_direction = "up"
                self.reached_limit = True
                self.current_floor = next_floor  # Move to the next floor

        return self.current_direction, next_floor, self.reached_limit

    def __look(self):
        next_request = self.lift_queue.dequeue(self.ignore_weight,self.is_lift_full())  # Gets the next request from the queue

        if next_request is None:
            return self.current_direction, self.current_floor

        next_floor = next_request.requested_floor

        if next_floor == self.current_floor:
            return self.current_direction, next_floor

        # If the lift is moving up and the requested floor is above the current floor
        if next_floor > self.current_floor and self.current_direction == "up":
            return self.current_direction, next_floor

        # If the lift is moving down and the requested floor is below the current floor
        elif next_floor < self.current_floor and self.current_direction == "down":
            return self.current_direction, next_floor

        # If the lift is moving in the wrong direction the direction is flipped
        elif self.current_direction == "up":
            return "down", next_floor

        elif self.current_direction == "down":
            return "up", next_floor

    def is_lift_full(self):
        return self.passenger_count >= self.capacity

    def get_free_space(self):
        return self.capacity - self.passenger_count

    def add_person(self):
        self.passenger_count += 1

    def remove_person(self):
        self.passenger_count -= 1
