class Lift:
    def __init__(self, total_floors, capacity):
        self.total_floors = total_floors
        self.capacity = capacity
        self.passenger_count = 0
        self.external_calls = {}
        self.internal_calls = set()

    def external_request(self, floor, direction):
        self.external_calls[floor] = [direction]

    def internal_request(self, floor):
        if self.passenger_count >= self.capacity:
            print("Lift is full! No more selections allowed.")
            # IDK WHAT TO DO HERE!!
            return
        self.internal_calls.add(floor)
        self.passenger_count += 1

    def clear_request(self, floor):
        self.external_calls.pop(floor)
        self.internal_calls.discard(floor)
        self.passenger_count -= 1

    def get_external_requests(self):
        return self.external_calls
    def get_internal_requests(self):
        return self.internal_calls
