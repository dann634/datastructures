from re import match

from Call import Call
from Heap import MinHeap
from LiftQueueCopy import LiftQueue
from AlgorithmEnum import Algorithm




class LiftManager:
    def __init__(self, capacity, direction, current_floor, floors, ignore_weight, use_priority_queue):
        self.capacity = capacity
        self.passenger_count = 0
        self.current_direction = direction
        self.current_floor = current_floor
        self.floors = floors
        self.ignore_weight = ignore_weight
        self.use_priority = use_priority_queue
        self.reached_limit = False
        self.lift_queue = None

    @staticmethod
    def get_instance(algorithm : Algorithm,
                     capacity, direction, current_floor, floors, ignore_weight, use_priority_queue
                     ):
        algorithm_obj = None

        match algorithm:
            case Algorithm.SCAN:
                algorithm_obj = LiftManagerSCAN(capacity, direction, current_floor, floors, ignore_weight, use_priority_queue)
            case Algorithm.LOOK:
                algorithm_obj = LiftManagerLOOK(capacity, direction, current_floor, floors, ignore_weight, use_priority_queue)
            case Algorithm.LLOOK:
                algorithm_obj = LiftManagerMyAlgorithm(capacity, direction, current_floor, floors, ignore_weight, use_priority_queue)

        return algorithm_obj

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

    def __init__(self, capacity, direction, current_floor, floors, ignore_weight, use_priority_queue):
        super().__init__(capacity, direction, current_floor, floors, ignore_weight, use_priority_queue)
        self.lift_queue = LiftQueue()


    def process_next_request(self):
        self.reached_limit = False  # Boolean to determine whether the lift has gone to the top or bottom of the building

        next_request: Call = self.lift_queue.dequeue(self.ignore_weight,
                                                     self.is_lift_full())  # Gets the next request from the queue

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

    def __init__(self, capacity, direction, current_floor, floors, ignore_weight, use_priority_queue):
        super().__init__(capacity, direction, current_floor, floors, ignore_weight, use_priority_queue)
        self.lift_queue = LiftQueue()



    def process_next_request(self):
        next_request = self.lift_queue.dequeue_look(
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

        # If the lift is moving up and the requested floor is above the current floor
        if next_floor > self.current_floor and self.current_direction == "up":
            return next_floor

        # If the lift is moving down and the requested floor is below the current floor
        elif next_floor < self.current_floor and self.current_direction == "down":
            return next_floor

        # If the lift is moving in the wrong direction the direction is flipped
        elif self.current_direction == "up":
            self.current_direction = "down"
            return next_floor

        elif self.current_direction == "down":
            self.current_direction = "up"
            return next_floor




class LiftManagerMyAlgorithm(LiftManager):
    def __init__(self, capacity, direction, current_floor, floors, ignore_weight, use_priority_queue):
        super().__init__(capacity, direction, current_floor, floors, ignore_weight, use_priority_queue)
        self.lift_queue = MinHeap()


    def process_next_request(self):
        next_request = self.lift_queue.dequeue(self.current_floor)  # Gets the next request from the queue

        if next_request is None:
            return self.current_floor

        next_floor = next_request

        if next_floor == self.current_floor:
            return next_floor

        # If the lift is moving up and the requested floor is above the current floor
        if next_floor > self.current_floor and self.current_direction == "up":
            return next_floor

        # If the lift is moving down and the requested floor is below the current floor
        elif next_floor < self.current_floor and self.current_direction == "down":
            return next_floor

        # If the lift is moving in the wrong direction the direction is flipped
        elif self.current_direction == "up":
            self.current_direction = "down"
            return next_floor

        elif self.current_direction == "down":
            self.current_direction = "up"
            return next_floor

