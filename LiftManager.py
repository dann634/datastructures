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

        if algorithm == Algorithm.SCAN:
            self.algorithm = self.__scan
        elif algorithm == Algorithm.LOOK:
            self.algorithm = self.__look

        #SCAN ONLY
        self.reached_limit = False



    def process_next_request(self):
        return self.algorithm()


    def __scan(self):

        self.reached_limit = False  # Boolean to determine whether the lift has gone to the top or bottom of the building

        # Should pass if lift is full to dequeue
        next_floor = self.lift_queue.dequeue(self.ignore_weight, self.is_lift_full()).requested_floor  # Gets the next floor from the queue

        at_target_floor = False  # Boolean to determine whether the lift has arrived at the next destination.
        while not at_target_floor:

            # If the lift is already at the requested floor or no request exists
            if next_floor == self.current_floor or next_floor is None:
                at_target_floor = True

            # If the lift is moving up and the requested floor is above the current floor
            elif next_floor > self.current_floor and self.current_direction == "up":
                at_target_floor = True

            # If the lift is moving down and the requested floor is below the current floor
            elif next_floor < self.current_floor and self.current_direction == "down":
                at_target_floor = True

            # If the lift cannot continue in the same direction, it reverses at the top or bottom of the building
            else:
                if self.current_direction == "up":
                    self.current_floor = self.floors  # Lift moves to the highest floor
                    self.current_direction = "down"  # Direction is changed to downwards

                elif self.current_direction == "down":
                    self.current_floor = self.floors  # Lift moves to the lowest floor
                    self.current_direction = "up"  # Direction is changed to upwards

                self.reached_limit = True  # Made true to show that the lift has gone to the top or bottom of the building

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
