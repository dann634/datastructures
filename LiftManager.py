import time
from re import match

from Call import Call
from Heap import MinHeap
from LiftQueue import LiftQueue
from AlgorithmEnum import Algorithm




class LiftManager:
    def __init__(self, capacity, direction, current_floor, floors, ignore_weight):
        self.capacity = capacity
        self.passenger_count = 0
        self.current_direction = direction
        self.current_floor = current_floor
        self.floors = floors
        self.ignore_weight = ignore_weight
        self.reached_limit = False
        self.lift_queue = None
        self.total_time = 0

    @staticmethod
    def get_instance(algorithm: Algorithm,
                     capacity : int,
                     direction : str,
                     current_floor : int,
                     floors : int,
                     ignore_weight : bool
                     ):

        algorithm_obj = None

        # Match case which calls the algorithm being used.
        match algorithm:
            case Algorithm.SCAN:
                algorithm_obj = LiftManagerSCAN(capacity, direction, current_floor, floors, ignore_weight)
            case Algorithm.LOOK:
                algorithm_obj = LiftManagerLOOK(capacity, direction, current_floor, floors, ignore_weight)
            case Algorithm.MYALGORITHM:
                algorithm_obj = LiftManagerMyAlgorithm(capacity, direction, current_floor, floors, ignore_weight)

        return algorithm_obj # Returns the next floor decided by the algorithm

    def process_next_request(self):
        pass

    def is_lift_full(self):
        return self.passenger_count >= self.capacity

    def get_free_space(self):
        return self.capacity - self.passenger_count

    def add_person(self):
        self.passenger_count += 1

    def remove_person(self):
        self.passenger_count -= 1



class LiftManagerSCAN(LiftManager):

    def __init__(self, capacity, direction, current_floor, floors, ignore_weight):
        super().__init__(capacity, direction, current_floor, floors, ignore_weight)
        self.lift_queue = LiftQueue()


    def process_next_request(self):
        self.reached_limit = False  # Boolean to determine whether the lift has gone to the top or bottom of the building

        next_request = self.lift_queue.dequeue(
            ignore_weight=self.ignore_weight,
            is_lift_full=self.is_lift_full(),
            current_floor=self.current_floor,
            direction=self.current_direction,
        )  # Gets the next request from the queue

        if next_request is None:
            return self.current_floor

        next_requested_floor = next_request.requested_floor

        # If the lift is already at the requested floor or no request exists
        if next_requested_floor == self.current_floor:
            return next_requested_floor

        if self.current_direction == "up" and next_requested_floor < self.current_floor:
            self.current_direction = "down"
            self.reached_limit = True

        elif self.current_direction == "down" and next_requested_floor > self.current_floor:
            self.current_direction = "up"
            self.reached_limit = True

        return next_requested_floor



class LiftManagerLOOK(LiftManager):

    def __init__(self, capacity, direction, current_floor, floors, ignore_weight):
        super().__init__(capacity, direction, current_floor, floors, ignore_weight)
        self.lift_queue = LiftQueue()



    def process_next_request(self):
        next_request = self.lift_queue.dequeue(
            ignore_weight=self.ignore_weight,
            is_lift_full=self.is_lift_full(),
            current_floor=self.current_floor,
            direction=self.current_direction,
        )  # Gets the next request from the queue

        if next_request is None:
            return self.current_floor

        next_floor = next_request.requested_floor

        if next_floor == self.current_floor:
            return next_floor

        # If the lift is moving in the wrong direction the direction is flipped
        elif next_floor < self.current_floor and self.current_direction == "up":
            self.current_direction = "down"
            return next_floor

        elif next_floor > self.current_floor and self.current_direction == "down":
            self.current_direction = "up"
            return next_floor

        return next_floor



class LiftManagerMyAlgorithm(LiftManager):
    def __init__(self, capacity, direction, current_floor, floors, ignore_weight):
        super().__init__(capacity, direction, current_floor, floors, ignore_weight)
        self.lift_queue = MinHeap()
        self.total_time = 0


    def process_next_request(self):
        next_floor = self.lift_queue.dequeue(self.current_floor)  # Gets the next request from the queue

        # Checks if the next request is None in order to avoid an error.
        if next_floor is None:
            return self.current_floor

        # Checks if the lift is already at the current floor.
        if next_floor == self.current_floor:
            return next_floor

        # If the lift is moving in the wrong direction the direction is flipped.
        elif next_floor < self.current_floor and self.current_direction == "up":
            self.current_direction = "down"
            return next_floor  # Returns the next floor to be served.

        # If the lift is moving in the wrong direction the direction is flipped.
        elif next_floor > self.current_floor and self.current_direction == "down":
            self.current_direction = "up"
            return next_floor  # Returns the next floor to be served.

        return next_floor  # Returns the next floor to be served.

