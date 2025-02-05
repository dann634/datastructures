from LiftQueue import LiftQueue
from Call import Call

class LiftManager:
    def __init__(self, total_floors, capacity, lift):
        self.total_floors = total_floors
        self.capacity = capacity
        self.passenger_count = 0
        self.call_queue = LiftQueue()


    def external_request(self, floor):
        self.call_queue.enqueue(Call(floor, False))

    def internal_request(self, floor):
        if self.passenger_count >= self.capacity:
            print("Lift is full! No more selections allowed.")
            # Modern lifts have sensors that now skip external requests
            return

        #Check if call already exists in queue before adding it again

        self.call_queue.enqueue(Call(floor, True))
        self.passenger_count += 1
